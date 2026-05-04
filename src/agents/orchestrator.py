"""Multi-agent orchestrator.

Routes queries to specialized agents (HR, Tech, Finance) based on content classification.
"""

import json
import re

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

from src.config import Settings
from src.tracing import get_langfuse_client
from src.vector_store import VectorStoreManager
from src.agents.hr_agent import HRAgent
from src.agents.tech_agent import TechAgent
from src.agents.finance_agent import FinanceAgent
from langfuse.langchain import CallbackHandler


CLASSIFICATION_PROMPT = """Eres un clasificador de intenciones para TechNova Solutions.
Analiza la consulta y clasifícala en: "hr", "tech", "finance", "unknown".

- "hr": RRHH, políticas de personal, beneficios (incluye stock options, seguros), vacaciones, onboarding (incluye setup de nuevo empleado), compensación, performance reviews, capacitación
- "tech": tecnología, soporte IT, configuración de software/hardware, acceso a sistemas, VPN, seguridad informática, incidentes de producción, repositorios de código
- "finance": finanzas, reembolsos, presupuestos, compras, facturas, viajes corporativos, impuestos, tarjetas corporativas, pagos a proveedores
- "unknown": no encaja en ninguna categoría

REGLA IMPORTANTE: Cuando una consulta sea ambigua entre dos dominios, clasifícala según el PROPÓSITO PRINCIPAL del usuario:
- "Set up my new laptop" durante onboarding → "hr" (el contexto es incorporación de empleado)
- "Tax implications of stock options" → "hr" (el contexto es un beneficio laboral, no contabilidad)
- "Fix a production server error" → "tech" (aunque tenga impacto financiero)

Responde SOLO con JSON: {{"intent": "...", "confidence": 0.0-1.0, "reasoning": "..."}}"""

VALID_INTENTS = ["hr", "tech", "finance", "unknown"]
_FALLBACK_RESULT = {
    "intent": "unknown",
    "confidence": 0.0,
    "reasoning": "Failed to parse classification",
}


def classify_intent(
    query: str,
    llm: ChatOpenAI,
    callbacks: list | None = None,
) -> dict:
    """Classify a user query into one of the domain intents.

    Args:
        query: The user's query string.
        llm: A ChatOpenAI instance used for classification.
        callbacks: Optional list of LangChain callbacks (e.g. Langfuse handler).

    Returns:
        A dict with keys:
            - intent (str): one of "hr", "tech", "finance", "unknown"
            - confidence (float): 0.0–1.0
            - reasoning (str): explanation of the classification
    """
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", CLASSIFICATION_PROMPT),
            ("human", "{query}"),
        ]
    )

    chain = prompt | llm

    try:
        response = chain.invoke(
            {"query": query},
            config={"callbacks": callbacks} if callbacks else {},
        )
        raw_content: str = response.content
    except Exception:
        return dict(_FALLBACK_RESULT)

    # Strip markdown code fences if present
    cleaned = re.sub(r"```(?:json)?\s*|\s*```", "", raw_content).strip()

    try:
        result = json.loads(cleaned)
    except (json.JSONDecodeError, ValueError):
        return dict(_FALLBACK_RESULT)

    # Validate and normalise intent
    intent = result.get("intent", "unknown")
    if intent not in VALID_INTENTS:
        intent = "unknown"

    # Validate and normalise confidence
    try:
        confidence = float(result.get("confidence", 0.0))
        confidence = max(0.0, min(1.0, confidence))
    except (TypeError, ValueError):
        confidence = 0.0

    reasoning = str(result.get("reasoning", ""))

    return {
        "intent": intent,
        "confidence": confidence,
        "reasoning": reasoning,
    }


class Orchestrator:
    """Routes user queries to the appropriate RAG agent based on intent classification.

    Initialises vector stores, sub-agents, and a shared LLM.  Each call to
    :meth:`route` creates a Langfuse parent trace and spans for the
    classification and RAG-retrieval phases so that the full pipeline is
    observable.
    """

    def __init__(self) -> None:
        settings = Settings()
        self.llm = ChatOpenAI(model=settings.MODEL_NAME, api_key=settings.OPENAI_API_KEY)
        self.langfuse = get_langfuse_client()

        # Initialize vector stores and retrievers
        vsm = VectorStoreManager()
        hr_retriever = vsm.get_retriever("hr_docs")
        tech_retriever = vsm.get_retriever("tech_docs")
        finance_retriever = vsm.get_retriever("finance_docs")

        # Initialize agents (no per-call langfuse_handler; callbacks injected at invoke time)
        self.agents: dict[str, HRAgent | TechAgent | FinanceAgent] = {
            "hr": HRAgent(hr_retriever, self.llm),
            "tech": TechAgent(tech_retriever, self.llm),
            "finance": FinanceAgent(finance_retriever, self.llm),
        }

    def route(self, query: str, user_id: str = "test-user") -> dict:
        """Classify *query* and dispatch it to the matching RAG agent.

        Creates a Langfuse parent trace that wraps two child spans:
        ``intent-classification`` and ``rag-retrieval``.

        Args:
            query: The user's question.
            user_id: Identifier used for the Langfuse trace (default "test-user").

        Returns:
            A dict with keys: ``query``, ``intent``, ``confidence``,
            ``reasoning``, ``answer``, ``sources``, ``agent``.
        """
        # 1. Create a stable trace_id for this request
        trace_id = self.langfuse.create_trace_id()

        with self.langfuse.start_as_current_observation(
            name="user-query",
            as_type="span",
            trace_context={"trace_id": trace_id},
            input=query,
        ):
            # Expose trace-level user info
            self.langfuse.set_current_trace_io(input=query)

            # Build a shared callback handler linked to this trace
            handler = CallbackHandler(trace_context={"trace_id": trace_id})

            # 2. Classify intent — child span
            with self.langfuse.start_as_current_observation(
                name="intent-classification",
                as_type="span",
                input=query,
            ):
                classification = classify_intent(query, self.llm, callbacks=[handler])
                intent: str = classification["intent"]
                confidence: float = classification["confidence"]
                reasoning: str = classification["reasoning"]
                self.langfuse.update_current_span(output=classification)

            # 3. Handle low-confidence warning
            if confidence < 0.5:
                self.langfuse.update_current_span(
                    metadata={"warning": f"Low confidence: {confidence}"}
                )

            # 4. Route to agent or return generic response
            if intent == "unknown":
                answer = (
                    "I'm not sure how to categorize your question. "
                    "Please try rephrasing or contact the appropriate department directly."
                )
                sources: list[str] = []
                agent_name = "none"
            else:
                # RAG retrieval — child span
                with self.langfuse.start_as_current_observation(
                    name="rag-retrieval",
                    as_type="span",
                    input={"query": query, "intent": intent},
                ):
                    agent = self.agents[intent]
                    result = agent.invoke(query)
                    answer = result["answer"]
                    sources = result["sources"]
                    agent_name = result["agent_name"]
                    self.langfuse.update_current_span(
                        output={"answer": answer, "sources": sources}
                    )

            # 5. Build response and update parent trace output
            response = {
                "query": query,
                "intent": intent,
                "confidence": confidence,
                "reasoning": reasoning,
                "answer": answer,
                "sources": sources,
                "agent": agent_name,
            }
            self.langfuse.set_current_trace_io(input=query, output=response)

        self.langfuse.flush()
        return response

    def batch_route(self, queries: list[dict]) -> dict:
        """Route a batch of queries and compute accuracy against expected intents.

        Args:
            queries: A list of dicts, each with a ``"query"`` key and an
                optional ``"expected_intent"`` and ``"user_id"`` key.

        Returns:
            A dict with keys:
                - ``results`` (list[dict]): per-query routing results.
                - ``accuracy`` (float | None): fraction correct over evaluated items.
                - ``total`` (int): total number of queries.
                - ``correct`` (int): number of correctly classified queries.
                - ``evaluated`` (int): number of queries that had an expected intent.
        """
        results: list[dict] = []
        correct = 0
        total_with_expected = 0

        for q in queries:
            query_text: str = q["query"]
            expected: str | None = q.get("expected_intent")

            try:
                result = self.route(query_text, user_id=q.get("user_id", "test-user"))
            except Exception as exc:
                result = {
                    "query": query_text,
                    "intent": "unknown",
                    "confidence": 0.0,
                    "reasoning": f"Error: {exc}",
                    "answer": "No se pudo procesar la consulta. Intenta de nuevo.",
                    "sources": [],
                    "agent": "none",
                }

            for key in ("id", "difficulty", "expected_keywords"):
                if key in q:
                    result[key] = q[key]

            if expected:
                total_with_expected += 1
                result["expected_intent"] = expected
                result["intent_match"] = result["intent"] == expected
                if result["intent_match"]:
                    correct += 1

            results.append(result)

        accuracy: float | None = (
            correct / total_with_expected if total_with_expected > 0 else None
        )

        return {
            "results": results,
            "accuracy": accuracy,
            "total": len(results),
            "correct": correct,
            "evaluated": total_with_expected,
        }

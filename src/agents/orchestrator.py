"""Multi-agent orchestrator.

Routes queries to specialized agents (HR, Tech, Finance) based on content classification.
"""

import json
import re

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate


CLASSIFICATION_PROMPT = """Eres un clasificador de intenciones para TechNova Solutions.
Analiza la consulta y clasifícala en: "hr", "tech", "finance", "unknown".

- "hr": RRHH, políticas de personal, beneficios, vacaciones, onboarding, compensación
- "tech": tecnología, soporte IT, configuración, acceso a sistemas, VPN, seguridad
- "finance": finanzas, reembolsos, presupuestos, compras, facturas, viajes
- "unknown": no encaja en ninguna categoría

Responde SOLO con JSON: {"intent": "...", "confidence": 0.0-1.0, "reasoning": "..."}"""

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

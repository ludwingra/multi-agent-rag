"""RAG system evaluator.

Evaluates response quality across 3 dimensions using an LLM judge and
sends scores to Langfuse for observability.
"""

import json

from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

EVAL_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are an expert evaluator of RAG (Retrieval-Augmented Generation) responses. "
            "Evaluate the assistant's answer on 3 dimensions, each scored 1-10:\n"
            "- relevance: does the answer directly address the user's question?\n"
            "- completeness: does it cover all important aspects of the question?\n"
            "- accuracy: is the answer grounded in the provided source documents?\n\n"
            "Return ONLY valid JSON with this exact structure:\n"
            '{{"relevance": <int>, "completeness": <int>, "accuracy": <int>, "summary": "<reasoning>"}}\n'
            "No extra text outside the JSON object.",
        ),
        (
            "human",
            "Question: {query}\n\n"
            "Intent: {intent}\n\n"
            "Sources consulted: {sources}\n\n"
            "Answer to evaluate:\n{answer}",
        ),
    ]
)


class ResponseEvaluator:
    def __init__(self, langfuse_client, llm):
        self._langfuse = langfuse_client
        self._llm = llm
        self._chain = EVAL_PROMPT | self._llm

    def evaluate_response(
        self,
        trace_id: str,
        query: str,
        answer: str,
        intent: str,
        sources: list[str],
    ) -> dict:
        sources_text = "\n".join(sources) if sources else "None"

        try:
            result = self._chain.invoke(
                {
                    "query": query,
                    "intent": intent,
                    "sources": sources_text,
                    "answer": answer,
                }
            )
            raw = result.content if hasattr(result, "content") else str(result)
            scores = json.loads(raw)
            relevance = float(scores["relevance"])
            completeness = float(scores["completeness"])
            accuracy = float(scores["accuracy"])
            summary = scores.get("summary", "")
        except Exception as exc:
            relevance = completeness = accuracy = 0.0
            summary = f"Evaluation failed: {exc}"

        overall = round((relevance + completeness + accuracy) / 3, 2)

        for name, value in [
            ("relevance", relevance),
            ("completeness", completeness),
            ("accuracy", accuracy),
            ("overall", overall),
        ]:
            self._langfuse.score(
                trace_id=trace_id,
                name=name,
                value=value,
                comment=summary,
            )

        return {
            "trace_id": trace_id,
            "query": query,
            "relevance": relevance,
            "completeness": completeness,
            "accuracy": accuracy,
            "overall": overall,
            "summary": summary,
        }

    def evaluate_batch(self, results: list[dict]) -> list[dict]:
        evaluations = []
        for result in results:
            evaluation = self.evaluate_response(
                trace_id=result.get("trace_id", ""),
                query=result.get("query", ""),
                answer=result.get("answer", ""),
                intent=result.get("intent", "unknown"),
                sources=result.get("sources", []),
            )
            evaluations.append(evaluation)
        return evaluations

    def generate_report(self, evaluations: list[dict]) -> str:
        if not evaluations:
            return "No evaluations to report."

        dims = ["relevance", "completeness", "accuracy", "overall"]
        averages = {
            dim: round(
                sum(e[dim] for e in evaluations) / len(evaluations), 2
            )
            for dim in dims
        }

        best = max(evaluations, key=lambda e: e["overall"])
        worst = min(evaluations, key=lambda e: e["overall"])

        lines = [
            "=" * 60,
            "RAG EVALUATION REPORT",
            f"Total responses evaluated: {len(evaluations)}",
            "=" * 60,
            "",
            "AVERAGES",
            f"  Relevance:    {averages['relevance']:.2f} / 10",
            f"  Completeness: {averages['completeness']:.2f} / 10",
            f"  Accuracy:     {averages['accuracy']:.2f} / 10",
            f"  Overall:      {averages['overall']:.2f} / 10",
            "",
            "BEST RESPONSE",
            f"  Query:   {best['query']}",
            f"  Overall: {best['overall']:.2f}",
            f"  Summary: {best['summary']}",
            "",
            "WORST RESPONSE",
            f"  Query:   {worst['query']}",
            f"  Overall: {worst['overall']:.2f}",
            f"  Summary: {worst['summary']}",
            "=" * 60,
        ]

        return "\n".join(lines)

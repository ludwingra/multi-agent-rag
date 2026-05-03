"""RAG system evaluator.

Evaluates retrieval quality and response accuracy using Langfuse traces.
"""


class RAGEvaluator:
    """Evaluates the multi-agent RAG system performance."""

    def evaluate_retrieval(self, query: str, expected_docs: list[str]) -> dict:
        """Evaluate document retrieval quality."""
        raise NotImplementedError

    def evaluate_response(self, query: str, response: str, ground_truth: str) -> dict:
        """Evaluate response accuracy against ground truth."""
        raise NotImplementedError

    def run_evaluation_suite(self) -> dict:
        """Run full evaluation suite and return metrics."""
        raise NotImplementedError

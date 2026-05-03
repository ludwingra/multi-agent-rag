"""Finance domain agent.

Handles queries about financial reports, budgets, accounting policies, etc.
"""


class FinanceAgent:
    """Specialized agent for finance-related queries."""

    def answer(self, query: str, context: list[str]) -> str:
        """Answer a finance query using provided context documents."""
        raise NotImplementedError

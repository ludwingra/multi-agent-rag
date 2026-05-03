"""HR domain agent.

Handles queries about human resources policies, benefits, hiring, etc.
"""


class HRAgent:
    """Specialized agent for HR-related queries."""

    def answer(self, query: str, context: list[str]) -> str:
        """Answer an HR query using provided context documents."""
        raise NotImplementedError

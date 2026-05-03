"""Technology domain agent.

Handles queries about technical documentation, architecture, APIs, etc.
"""


class TechAgent:
    """Specialized agent for technology-related queries."""

    def answer(self, query: str, context: list[str]) -> str:
        """Answer a tech query using provided context documents."""
        raise NotImplementedError

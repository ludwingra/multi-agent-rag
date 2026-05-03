"""Multi-agent orchestrator.

Routes queries to specialized agents (HR, Tech, Finance) based on content classification.
"""


class OrchestratorAgent:
    """Routes user queries to the appropriate domain-specific agent."""

    def route(self, query: str) -> str:
        """Classify and route a query to the appropriate agent."""
        raise NotImplementedError

    def run(self, query: str) -> str:
        """Process a query end-to-end: route, execute, return response."""
        raise NotImplementedError

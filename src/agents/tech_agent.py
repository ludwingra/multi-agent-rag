from langchain_openai import ChatOpenAI
from langchain_core.vectorstores import VectorStoreRetriever
from src.agents.base_agent import BaseRAGAgent


class TechAgent(BaseRAGAgent):
    def __init__(self, retriever: VectorStoreRetriever, llm: ChatOpenAI, langfuse_handler=None):
        super().__init__(retriever, llm, agent_name="tech_agent", domain="tech", langfuse_handler=langfuse_handler)

    def get_system_prompt(self) -> str:
        return (
            "You are a Technical Support specialist at TechNova Solutions. "
            "Help with technical documentation, system architecture, API usage, troubleshooting, and configuration. "
            "Provide step-by-step instructions when applicable. "
            "Base your answers ONLY on the provided context documents. "
            "If the issue requires hands-on intervention, suggest escalating to the engineering team."
        )

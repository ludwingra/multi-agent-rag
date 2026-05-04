from langchain_openai import ChatOpenAI
from langchain_core.vectorstores import VectorStoreRetriever
from src.agents.base_agent import BaseRAGAgent


class HRAgent(BaseRAGAgent):
    def __init__(self, retriever: VectorStoreRetriever, llm: ChatOpenAI, langfuse_handler=None):
        super().__init__(retriever, llm, agent_name="hr_agent", domain="hr", langfuse_handler=langfuse_handler)

    def get_system_prompt(self) -> str:
        return (
            "You are an HR specialist at TechNova Solutions. "
            "Answer questions about HR policies, benefits, hiring, onboarding, compensation, and employee programs. "
            "Base your answers ONLY on the provided context documents. "
            "If you cannot find the information in the context, say so and suggest contacting the HR department directly."
        )

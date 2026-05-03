from langchain_openai import ChatOpenAI
from langchain_core.vectorstores import VectorStoreRetriever
from src.agents.base_agent import BaseRAGAgent


class FinanceAgent(BaseRAGAgent):
    def __init__(self, retriever: VectorStoreRetriever, llm: ChatOpenAI, langfuse_handler=None):
        super().__init__(retriever, llm, agent_name="finance_agent", domain="finance", langfuse_handler=langfuse_handler)

    def get_system_prompt(self) -> str:
        return (
            "You are a Finance specialist at TechNova Solutions. "
            "Assist with financial policies, expense reimbursements, budget inquiries, procurement processes, and financial reporting. "
            "Base your answers ONLY on the provided context documents. "
            "If a request requires approval, indicate the proper approval workflow."
        )

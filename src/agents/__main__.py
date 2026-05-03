from dotenv import load_dotenv
load_dotenv()

from src.config import Settings
from langchain_openai import ChatOpenAI
from src.vector_store import VectorStoreManager, DOMAINS
from src.agents import HRAgent, TechAgent, FinanceAgent

settings = Settings()
llm = ChatOpenAI(model=settings.MODEL_NAME)
vsm = VectorStoreManager()

agent_configs = [
    ("hr", DOMAINS["hr"][1], HRAgent, "What are the employee benefits at TechNova?"),
    ("tech", DOMAINS["tech"][1], TechAgent, "How do I configure API access?"),
    ("finance", DOMAINS["finance"][1], FinanceAgent, "What is the expense reimbursement process?"),
]

for domain, collection_name, AgentClass, query in agent_configs:
    retriever = vsm.get_retriever(collection_name, k=3)
    agent = AgentClass(retriever=retriever, llm=llm)
    result = agent.invoke(query)
    print(f"[{result['agent_name']}] domain={result['domain']}")
    print(f"  answer: {result['answer'][:200]}")
    print(f"  sources: {len(result['sources'])}")

print("Smoke test complete.")

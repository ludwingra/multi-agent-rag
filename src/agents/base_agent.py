from abc import ABC, abstractmethod

from langchain_openai import ChatOpenAI
from langchain_core.documents import Document
from langchain_core.vectorstores import VectorStoreRetriever
from langchain_classic.chains.combine_documents.stuff import create_stuff_documents_chain
from langchain_classic.chains.retrieval import create_retrieval_chain
from langchain_core.prompts import ChatPromptTemplate


class BaseRAGAgent(ABC):

    def __init__(
        self,
        retriever: VectorStoreRetriever,
        llm: ChatOpenAI,
        agent_name: str,
        domain: str,
        langfuse_handler=None,
    ):
        self.retriever = retriever
        self.llm = llm
        self.agent_name = agent_name
        self.domain = domain
        self.langfuse_handler = langfuse_handler

        system_prompt = self.get_system_prompt()
        prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt + "\n\nUse the following context to answer:\n\n{context}"),
            ("human", "{input}"),
        ])

        question_answer_chain = create_stuff_documents_chain(llm, prompt)
        self.chain = create_retrieval_chain(retriever, question_answer_chain)

    @abstractmethod
    def get_system_prompt(self) -> str:
        pass

    def invoke(self, query: str) -> dict:
        callbacks = []
        if self.langfuse_handler:
            callbacks.append(self.langfuse_handler)

        try:
            result = self.chain.invoke(
                {"input": query},
                config={"callbacks": callbacks},
            )
            answer = result["answer"]
            sources = []
            for doc in result.get("context", []):
                if isinstance(doc, Document):
                    source = doc.metadata.get("source_file") or doc.page_content[:100]
                else:
                    source = str(doc)[:100]
                sources.append(source)
        except Exception:
            answer = "I couldn't find relevant information to answer your question."
            sources = []

        return {
            "answer": answer,
            "sources": sources,
            "agent_name": self.agent_name,
            "domain": self.domain,
        }

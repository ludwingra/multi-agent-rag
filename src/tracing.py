from langfuse.langchain import CallbackHandler
from langfuse import Langfuse
from src.config import Settings


def get_langfuse_handler(trace_name: str, user_id: str = "test-user") -> CallbackHandler:
    settings = Settings()
    return CallbackHandler(
        public_key=settings.LANGFUSE_PUBLIC_KEY,
        secret_key=settings.LANGFUSE_SECRET_KEY,
        host=settings.LANGFUSE_HOST,
        trace_name=trace_name,
        user_id=user_id,
    )


def get_langfuse_client() -> Langfuse:
    settings = Settings()
    return Langfuse(
        public_key=settings.LANGFUSE_PUBLIC_KEY,
        secret_key=settings.LANGFUSE_SECRET_KEY,
        host=settings.LANGFUSE_HOST,
    )

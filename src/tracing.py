from langfuse.langchain import CallbackHandler
from langfuse import Langfuse
from src.config import Settings


def _get_host(settings: Settings) -> str:
    return settings.LANGFUSE_HOST or settings.LANGFUSE_BASE_URL


def get_langfuse_handler(trace_name: str, user_id: str = "test-user") -> CallbackHandler:
    settings = Settings()
    return CallbackHandler(
        public_key=settings.LANGFUSE_PUBLIC_KEY,
        secret_key=settings.LANGFUSE_SECRET_KEY,
        host=_get_host(settings),
        trace_name=trace_name,
        user_id=user_id,
    )


def get_langfuse_client() -> Langfuse:
    settings = Settings()
    return Langfuse(
        public_key=settings.LANGFUSE_PUBLIC_KEY,
        secret_key=settings.LANGFUSE_SECRET_KEY,
        host=_get_host(settings),
    )

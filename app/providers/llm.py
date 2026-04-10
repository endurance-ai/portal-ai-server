from typing import ClassVar

import httpx

from app.core.config import settings


class LLMProvider:
    """LiteLLM 프록시 클라이언트"""

    _client: ClassVar[httpx.AsyncClient | None] = None

    @classmethod
    def get_client(cls) -> httpx.AsyncClient:
        if cls._client is None:
            cls._client = httpx.AsyncClient(
                base_url=settings.LITELLM_BASE_URL,
                timeout=10.0,
            )
        return cls._client

    @classmethod
    async def check_connection(cls) -> bool:
        """LiteLLM 프록시 연결 확인."""
        try:
            client = cls.get_client()
            resp = await client.get("/health")
            return resp.status_code == 200
        except Exception:
            return False

    @classmethod
    async def close(cls) -> None:
        if cls._client is not None:
            await cls._client.aclose()
            cls._client = None

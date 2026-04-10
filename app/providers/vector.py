from typing import ClassVar

from qdrant_client import AsyncQdrantClient

from app.core.config import settings


class VectorProvider:
    """Qdrant 벡터 DB 클라이언트 (싱글톤)"""

    _client: ClassVar[AsyncQdrantClient | None] = None

    @classmethod
    def get_client(cls) -> AsyncQdrantClient:
        if cls._client is None:
            cls._client = AsyncQdrantClient(
                url=settings.qdrant_url,
                timeout=10,
            )
        return cls._client

    @classmethod
    async def check_connection(cls) -> bool:
        """Qdrant 연결 확인. 연결되면 True, 실패하면 False."""
        try:
            client = cls.get_client()
            await client.get_collections()
            return True
        except Exception:
            return False

    @classmethod
    async def close(cls) -> None:
        if cls._client is not None:
            await cls._client.close()
            cls._client = None

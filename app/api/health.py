from fastapi import APIRouter
from fastapi.responses import ORJSONResponse

from app.core.config import settings
from app.providers.llm import LLMProvider
from app.providers.vector import VectorProvider

router = APIRouter()


@router.get("/health")
async def health_check() -> ORJSONResponse:
    qdrant_ok = await VectorProvider.check_connection()
    litellm_ok = await LLMProvider.check_connection()

    all_ok = qdrant_ok and litellm_ok
    status_code = 200 if all_ok else 503

    return ORJSONResponse(
        status_code=status_code,
        content={
            "status": "ok" if all_ok else "degraded",
            "qdrant": "connected" if qdrant_ok else "disconnected",
            "litellm": "connected" if litellm_ok else "disconnected",
            "version": settings.VERSION,
        },
    )

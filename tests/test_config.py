from app.core.config import Settings


def test_settings_defaults():
    """기본값으로 Settings 생성 가능해야 한다."""
    s = Settings(
        QDRANT_HOST="localhost",
        QDRANT_PORT=6333,
        LITELLM_BASE_URL="http://localhost:4000",
    )
    assert s.QDRANT_HOST == "localhost"
    assert s.QDRANT_PORT == 6333
    assert s.LITELLM_BASE_URL == "http://localhost:4000"
    assert s.PROJECT_NAME == "portal-ai-server"
    assert s.ENVIRONMENT == "development"


def test_settings_qdrant_url():
    """qdrant_url 프로퍼티가 host:port를 결합해야 한다."""
    s = Settings(
        QDRANT_HOST="qdrant",
        QDRANT_PORT=6333,
        LITELLM_BASE_URL="http://litellm:4000",
    )
    assert s.qdrant_url == "http://qdrant:6333"

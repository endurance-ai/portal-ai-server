# portal-ai-server

Portal.ai 패션 추천 AI 서버 — FastAPI 기반 검색 + 리파인 파이프라인. Next.js에서 Vision 분석 완료된 아이템을 받아 Qdrant 벡터 검색 + enum 스코어링 후 product_id 리턴.

## 프로젝트 구조

```
app/
├── main.py              # FastAPI 앱 + lifespan + CORS
├── api/                 # 라우트 (recommend, health)
├── pipeline/            # 파이프라인 스텝 (enhance, search, response, metadata)
├── scoring/             # enum 스코어링 (fashion-ai TS → Python 포팅)
├── providers/           # 외부 서비스 클라이언트 (LLM, embedding, Qdrant)
└── models/              # Pydantic request/response
scripts/                 # 배치 스크립트 (임베딩 등)
```

## 기술 스택

| 영역 | 기술 |
|------|------|
| 프레임워크 | FastAPI + uvicorn |
| LLM/임베딩 | LiteLLM → OpenAI / Cohere / Bedrock |
| 벡터 DB | Qdrant (Docker, dense vector) |
| 스키마 | Pydantic v2 |
| HTTP | httpx (async) |
| 패키지 | uv |
| 린트 | ruff |
| 테스트 | pytest + pytest-asyncio |
| 컨테이너 | Docker Compose (ai-server + litellm + qdrant + nginx) |

## 개발 명령어

```bash
uv sync                      # 의존성 설치
uv run uvicorn app.main:app --reload --port 8000  # 로컬 실행
uv run ruff check .          # 린트
uv run ruff format .         # 포맷
uv run pytest                # 테스트
docker compose up -d         # 전체 스택 기동
```

## 코딩 컨벤션

- plain async 함수 체인 (LangGraph/LangChain 사용 금지, MVP)
- Pydantic v2 모델로 request/response 정의
- LLM 호출은 반드시 LiteLLM 프록시 경유 (localhost:4000)
- 임베딩도 LiteLLM 경유 (프로바이더 교체 용이)
- ruff로 린트+포맷 (line-length=120)

## 핵심 파일

| 파일 | 설명 |
|------|------|
| `app/main.py` | FastAPI 앱 엔트리포인트 |
| `app/api/recommend.py` | POST /recommend 메인 엔드포인트 |
| `app/pipeline/enhance.py` | 쿼리 개선 (리파인 핵심, LLM 호출) |
| `app/pipeline/search.py` | Qdrant 벡터 검색 + enum 스코어링 결합 |
| `app/scoring/enum_scorer.py` | 13차원 가중치 스코어링 (TS에서 포팅) |
| `app/scoring/weights.py` | 스코어링 가중치 상수 |
| `app/providers/vector.py` | AsyncQdrantClient 래퍼 |
| `app/providers/llm.py` | LiteLLM 클라이언트 |
| `app/models/request.py` | RecommendRequest (AnalyzedItem 포함) |
| `app/models/response.py` | RecommendResponse |
| `scripts/batch_embed.py` | 26K 상품 임베딩 배치 |
| `litellm-config.yaml` | LLM/임베딩 모델 라우팅 설정 |

## 검색 전략

```
최종 스코어 = vector_score × 0.4 + enum_score × 0.6
```

- dense vector: Qdrant 코사인 유사도 (임베딩 API)
- enum score: 13차원 가중치 (카테고리/색상/핏/소재/스타일/시즌/패턴 등)
- 다양성: 브랜드 max 2, 플랫폼 max 3, 아이템당 top 7

## 인증 구조

AI 서버는 stateless. 인증 없음.
Next.js가 세션 관리 + Supabase Auth 담당 → AI 서버에 request body로 전달.

## 환경 변수

`.env.example` 참조. LiteLLM 프록시를 경유하므로 API 키는 LiteLLM 컨테이너에만 설정.

## 상세 참조 문서

| 문서 | 내용 |
|------|------|
| `docs/plans/2026-04-10-ai-server-design.md` | AI 서버 설계 스펙 (아키텍처, API, 파이프라인, 벡터 검색) |
| `docs/plans/26-04-10-ai-server-bootstrap-guide.md` | 부트스트랩 가이드 (참고 프로젝트, 포팅 대상, 구현 순서) |

## 참고 프로젝트

| 프로젝트 | 경로 | 참고 대상 |
|----------|------|----------|
| seed-lognia | `/Users/hansangho/Desktop/seed-lognia` | FastAPI 구조, Provider 패턴, Qdrant 사용 |
| fashion-ai | `/Users/hansangho/Desktop/fashion-ai` | 포팅 원본 (검색 로직, enum, 프롬프트) |
| aws-infra | `/Users/hansangho/Desktop/aws-infra` | LiteLLM Docker/설정, EC2 셋업 |

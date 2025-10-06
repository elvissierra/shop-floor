from __future__ import annotations
import logging
import strawberry
from fastapi import Depends, FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from strawberry.fastapi import GraphQLRouter
from core import Mutation, Query
from app.core.config import settings
from app.core.database import SessionLocal

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s [%(name)s] %(message)s")
log = logging.getLogger("shop-floor")

schema = strawberry.Schema(query=Query, mutation=Mutation)
app = FastAPI(title=settings.PROJECT_NAME)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Per-request DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

async def get_context(request: Request):
    # allocate a per-request session for GraphQL
    db_gen = get_db()
    db = next(db_gen)
    request.state._db_gen = db_gen
    request.state.db = db
    return {"db": db}

@app.middleware("http")
async def close_db_after_request(request: Request, call_next):
    try:
        return await call_next(request)
    finally:
        db_gen = getattr(request.state, "_db_gen", None)
        if db_gen:
            try:
                next(db_gen)
            except StopIteration:
                pass

graphql_app = GraphQLRouter(schema, context_getter=get_context)
app.include_router(graphql_app, prefix="/graphql")

# Health & readiness
@app.get("/healthz")
def healthz():
    return {"status": "ok"}

@app.get("/readyz")
def readyz():
    if not settings.DATABASE_URL:
        return JSONResponse(status_code=500, content={"status": "error", "reason": "no DATABASE_URL"})
    return {"status": "ready"}

# Error normalization
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(status_code=422, content={"detail": exc.errors()})

@app.get("/")
def ping():
    return {"ping": "ok"}
from __future__ import annotations
import logging
import strawberry
from strawberry.schema.config import StrawberryConfig
from fastapi import Depends, FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from strawberry.fastapi import GraphQLRouter
from core import Mutation, Query
from app.core.config import settings
from sqlalchemy import text
from app.core.database import SessionLocal, engine



logging.basicConfig(
    level=logging.INFO, format="%(asctime)s %(levelname)s [%(name)s] %(message)s"
)
log = logging.getLogger("shop-floor")

def _as_list(v):
    if isinstance(v, str):
        return [s.strip() for s in v.split(",") if s.strip()]
    return v

schema = strawberry.Schema(
    query=Query,
    mutation=Mutation,
    config=StrawberryConfig(auto_camel_case=True),
)
app = FastAPI(title=settings.PROJECT_NAME)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=_as_list(settings.BACKEND_CORS_ORIGINS),
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


# --- GraphQL error formatting with codes ---
def graphql_error_formatter(error):
    # Try to unwrap the original exception raised in resolvers/services
    original = getattr(error, "original_error", None) or error
    message = str(original) if original else str(error)

    code = "INTERNAL_SERVER_ERROR"
    # Convention: prefix messages in services with "NOT_FOUND:", "CONFLICT:", "VALIDATION:"
    if isinstance(message, str):
        if message.startswith("NOT_FOUND:"):
            code = "NOT_FOUND"
            message = message.split(":", 1)[1].strip()
        elif message.startswith("CONFLICT:"):
            code = "CONFLICT"
            message = message.split(":", 1)[1].strip()
        elif message.startswith("VALIDATION:"):
            code = "BAD_REQUEST"
            message = message.split(":", 1)[1].strip()

    # Build a GraphQL-compliant error dict with extensions.code
    return {
        "message": message,
        "locations": getattr(error, "locations", None),
        "path": getattr(error, "path", None),
        "extensions": {"code": code},
    }


try:
    graphql_app = GraphQLRouter(
        schema,
        context_getter=get_context,
        error_formatter=graphql_error_formatter,  # newer Strawberry
    )
except TypeError:
    graphql_app = GraphQLRouter(
        schema,
        context_getter=get_context,
    )
app.include_router(graphql_app, prefix="/graphql")


# Health & readiness
@app.get("/healthz")
def healthz():
    return {"status": "ok"}


@app.get("/readyz")
def readyz():
    if not settings.DATABASE_URL:
        return JSONResponse(status_code=500, content={"status": "error", "reason": "no DATABASE_URL"})
    try:
        with engine.connect() as conn:
            conn.execute(text("select 1"))
        return {"status": "ready"}
    except Exception as e:
        return JSONResponse(status_code=500, content={"status": "error", "reason": str(e)})


# Error normalization
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(status_code=422, content={"detail": exc.errors()})


@app.get("/")
def ping():
    return {"ping": "ok"}

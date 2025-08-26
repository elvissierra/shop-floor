import strawberry
from fastapi import FastAPI, Request
from strawberry.fastapi import GraphQLRouter
from backend.core import Mutation, Query
from backend.app.core.database import get_db, SessionLocal
from fastapi.middleware.cors import CORSMiddleware


schema = strawberry.Schema(query=Query, mutation=Mutation)

app = FastAPI()

# Enable CORS for local dev (GraphQL UI / frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    try:
        response = await call_next(request)
        return response
    finally:    
        db = getattr(request.state, "db", None)
        if db is not None:
            db.close()


async def get_context(request: Request):
    db = SessionLocal()
    request.state.db = db
    return {"db": db}


graphql_app = GraphQLRouter(schema, context_getter=get_context)
app.include_router(graphql_app, prefix="/graphql")


@app.get("/")
def ping():
    return {"ping": "has been pinged"}

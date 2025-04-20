import strawberry
from fastapi import FastAPI, Depends
from strawberry.fastapi import GraphQLRouter
from core import Mutation, Query
from config.database import get_db


schema = strawberry.Schema(query=Query, mutation=Mutation)


def get_context(db=Depends(get_db)):
    return {"db": db}


graphql_app = GraphQLRouter(schema, context_getter=get_context)
app = FastAPI()
app.include_router(graphql_app, prefix="/graphql")


@app.get("/")
def ping():
    return {"ping": "has been pinged"}

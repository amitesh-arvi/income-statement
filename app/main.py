from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.datasource import load_ledger


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.ledger = load_ledger()
    yield


app = FastAPI(title="Income Statement", lifespan=lifespan)


@app.get("/")
def hello_world():
    return {"message": "Hello World"}

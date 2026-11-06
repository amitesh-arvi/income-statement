from contextlib import asynccontextmanager
from datetime import date

from fastapi import FastAPI, HTTPException, Request

from app.datasource import load_ledger
from app.income_statement import calculate_income_statement
from app.models import IncomeStatement


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.ledger = load_ledger()
    yield


app = FastAPI(title="Income Statement", lifespan=lifespan)


@app.get("/")
def hello_world():
    return {"message": "Hello World"}


@app.get("/income-statement", response_model=IncomeStatement)
def income_statement(request: Request, start: date, end: date) -> IncomeStatement:
    if start > end:
        raise HTTPException(
            status_code=422, detail="Start date must be on or before end date."
        )

    return calculate_income_statement(request.app.state.ledger, start, end)

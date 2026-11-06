from contextlib import asynccontextmanager
from datetime import date
from decimal import Decimal
from pathlib import Path

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.datasource import load_ledger
from app.income_statement import calculate_income_statement
from app.models import IncomeStatement


templates = Jinja2Templates(directory=Path(__file__).resolve().parent / "templates")


def format_money(amount: Decimal) -> str:
    if amount < 0:
        return f"({abs(amount):,.2f})"
    return f"{amount:,.2f}"


templates.env.filters["money"] = format_money


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.ledger = load_ledger()
    yield


app = FastAPI(title="Income Statement", lifespan=lifespan)


@app.get("/", response_class=HTMLResponse)
def statement_page(
    request: Request, start: str = "2026-01-01", end: str = "2026-03-31"
):
    ledger = request.app.state.ledger
    statement = None
    error = None

    try:
        start_date = date.fromisoformat(start)
        end_date = date.fromisoformat(end)
    except ValueError:
        error = "Enter a valid start and end date."
    else:
        if start_date > end_date:
            error = "Start date must be on or before end date."
        else:
            statement = calculate_income_statement(ledger, start_date, end_date)

    return templates.TemplateResponse(
        request=request,
        name="income_statement.html",
        context={
            "company": ledger.company,
            "currency": ledger.currency,
            "start": start,
            "end": end,
            "statement": statement,
            "error": error,
        },
        status_code=422 if error else 200,
    )


@app.get("/income-statement", response_model=IncomeStatement)
def income_statement(request: Request, start: date, end: date) -> IncomeStatement:
    if start > end:
        raise HTTPException(
            status_code=422, detail="Start date must be on or before end date."
        )

    return calculate_income_statement(request.app.state.ledger, start, end)

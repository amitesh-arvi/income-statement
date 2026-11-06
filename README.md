# Income Statement

A FastAPI app that displays an income statement for a selected date range using the supplied ledger.

## Setup on macOS

Install uv if needed:

```sh
brew install uv
```

From the repository directory, install the locked dependencies:

```sh
uv sync --python 3.13 --locked
```

uv downloads Python if needed and creates the virtual environment automatically.

## Run the backend and frontend

```sh
uv run fastapi dev app/main.py
```

This single command serves both the Jinja frontend and the API.

- Frontend: http://127.0.0.1:8000 — select dates and click **Show statement**. Defaults to Q1 2026.
- API docs: http://127.0.0.1:8000/docs
- Income statement: http://127.0.0.1:8000/income-statement?start=2026-01-01&end=2026-03-31

## Run tests

```sh
uv run python -m pytest
```

## Versions used

Python 3.13.5, uv 0.11.21, FastAPI 0.162.0, and pytest 9.2.0. Dependency versions are recorded in `uv.lock`.

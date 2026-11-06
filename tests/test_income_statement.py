from datetime import date
from decimal import Decimal

import pytest

from app.datasource import load_ledger
from app.income_statement import calculate_income_statement


@pytest.fixture
def ledger():
    return load_ledger()


def test_q1_sections_and_account_amounts(ledger):
    statement = calculate_income_statement(ledger, date(2026, 1, 1), date(2026, 3, 31))
    assert statement.revenue.total == Decimal("37850.50")
    assert statement.cost_of_goods_sold.total == Decimal("14272.75")
    assert statement.gross_profit == Decimal("23577.75")
    assert statement.operating_expenses.total == Decimal("68100.07")
    assert statement.operating_income == Decimal("-44522.32")
    assert statement.other_income.total == Decimal("42.18")
    assert statement.net_income == Decimal("-44480.14")
    sections = [statement.revenue, statement.cost_of_goods_sold,
                statement.operating_expenses, statement.other_income]
    amounts = {account.number: account.amount
               for section in sections for account in section.accounts}
    assert amounts == {
        "4000": Decimal("35650.75"), "4100": Decimal("3000.00"),
        "4900": Decimal("-800.25"), "5000": Decimal("14272.75"),
        "6000": Decimal("55500.00"), "6100": Decimal("9000.00"),
        "6200": Decimal("1099.97"), "6300": Decimal("2500.10"),
        "7000": Decimal("42.18"),
    }


@pytest.mark.parametrize(("day", "expected"), [
    ("2026-01-01", "-9000.00"),  # Entire rent expense on the recorded date.
    ("2026-01-10", "0.00"),  # Annual billing touches only balance-sheet accounts.
    ("2026-02-03", "4920.00"),  # Posted sale and COGS, excluding duplicate void sale.
    ("2026-02-14", "-650.25"),  # Return reduces revenue.
    ("2026-02-15", "0.00"),  # Collecting a receivable creates no revenue.
    ("2026-03-15", "0.00"),  # Draft bonus is excluded.
    ("2026-03-20", "100.00"),  # Vendor credit reduces expense.
    ("2026-03-31", "-17457.82"),  # Inclusive end date.
])
def test_single_day_activity(ledger, day, expected):
    day = date.fromisoformat(day)
    statement = calculate_income_statement(ledger, day, day)
    assert statement.net_income == Decimal(expected)


def test_empty_period_keeps_accounts_and_zero_totals(ledger):
    statement = calculate_income_statement(ledger, date(2030, 1, 1), date(2030, 1, 31))
    assert statement.net_income == Decimal("0.00")
    assert len(statement.operating_expenses.accounts) == 4
    assert all(account.amount == 0 for account in statement.operating_expenses.accounts)


def test_reversed_period(ledger):
    with pytest.raises(ValueError):
        calculate_income_statement(ledger, date(2026, 3, 31), date(2026, 1, 1))

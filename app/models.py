from datetime import date
from decimal import Decimal
from enum import StrEnum

from pydantic import BaseModel, Field


class AccountType(StrEnum):
    ASSET = "asset"
    LIABILITY = "liability"
    EQUITY = "equity"
    REVENUE = "revenue"
    EXPENSE = "expense"


class AccountSubtype(StrEnum):
    OPERATING_REVENUE = "operating_revenue"
    CONTRA_REVENUE = "contra_revenue"
    COGS = "cogs"
    OPERATING_EXPENSE = "operating_expense"
    OTHER_INCOME = "other_income"
    BALANCE_SHEET = "balance_sheet"


class EntryStatus(StrEnum):
    POSTED = "posted"
    DRAFT = "draft"
    VOID = "void"


class Account(BaseModel):
    number: str
    name: str
    type: AccountType
    subtype: AccountSubtype
    is_active: bool


class JournalLine(BaseModel):
    account: str
    debit: Decimal = Field(ge=0, allow_inf_nan=False)
    credit: Decimal = Field(ge=0, allow_inf_nan=False)


class JournalEntry(BaseModel):
    id: str
    date: date
    status: EntryStatus
    memo: str
    lines: list[JournalLine]


class Ledger(BaseModel):
    company: str
    currency: str
    accounts: list[Account]
    journal_entries: list[JournalEntry]

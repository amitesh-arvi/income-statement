from datetime import date
from decimal import Decimal

from app.models import (
    AccountSubtype,
    AccountType,
    EntryStatus,
    IncomeStatement,
    Ledger,
    StatementAccount,
    StatementSection,
)


SECTION_BY_SUBTYPE = {
    AccountSubtype.OPERATING_REVENUE: "revenue",
    AccountSubtype.CONTRA_REVENUE: "revenue",
    AccountSubtype.COGS: "cost_of_goods_sold",
    AccountSubtype.OPERATING_EXPENSE: "operating_expenses",
    AccountSubtype.OTHER_INCOME: "other_income",
}


def calculate_income_statement(ledger: Ledger, start: date, end: date) -> IncomeStatement:
    if start > end:
        raise ValueError("Start date must be on or before end date.")

    accounts_by_number = {account.number: account for account in ledger.accounts}
    totals = {account.number: Decimal("0.00") for account in ledger.accounts}

    for entry in ledger.journal_entries:
        if entry.status != EntryStatus.POSTED or not start <= entry.date <= end:
            continue

        for line in entry.lines:
            account = accounts_by_number[line.account]
            if account.type == AccountType.REVENUE:
                totals[account.number] += line.credit - line.debit
            elif account.type == AccountType.EXPENSE:
                totals[account.number] += line.debit - line.credit

    sections = {name: StatementSection() for name in SECTION_BY_SUBTYPE.values()}
    for account in sorted(ledger.accounts, key=lambda account: account.number):
        if account.type not in {AccountType.REVENUE, AccountType.EXPENSE}:
            continue

        section = sections[SECTION_BY_SUBTYPE[account.subtype]]
        amount = totals[account.number]
        section.accounts.append(
            StatementAccount(number=account.number, name=account.name, amount=amount)
        )
        section.total += amount

    gross_profit = sections["revenue"].total - sections["cost_of_goods_sold"].total
    operating_income = gross_profit - sections["operating_expenses"].total
    net_income = operating_income + sections["other_income"].total

    return IncomeStatement(
        company=ledger.company,
        currency=ledger.currency,
        start=start,
        end=end,
        **sections,
        gross_profit=gross_profit,
        operating_income=operating_income,
        net_income=net_income,
    )

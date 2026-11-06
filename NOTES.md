# Notes

## Q1 2026 result

Net income for **2026-01-01 through 2026-03-31 is -$44,480.14 USD**, a net loss.

## Decisions and assumptions

- Initially, I had thought about using Streamlit for the UI but since server rendered pages were fine, decided to use FastAPI for hosting the frontend and the backend
- Use `Decimal` for money and decimal strings in JSON.
- I initially considered a flat JSON response, which would require some grouping in the frontend. I chose a shallow nested response to keep each section’s accounts and subtotal together, making them easier to render.
- Load the ledger once at startup. The API and Jinja page share the calculation function.
- Include only posted journal entries. Both the start and end dates are inclusive.
- Include historical activity on inactive accounts because inactivity only prevents new postings.
- Show accounts with zero activity to keep the statement layout consistent across date ranges.
- Follow entries as recorded. The full $9,000 rent expense belongs to January 1, and subscription revenue counts when recognition entries are posted.

## Verification

Aside from the unit tests for the income calculation function and the test for the API and the pages, I used a calculator to make sure that the numbers add up correctly. 

## AI usage

Most of my time was spent understanding accounting concepts. Since I am new to the field, I wanted to ensure that I have a good grasp of the data and the calculations that needed to be done. I was clear that I wanted to use FastAPI for this implementation since it gives enough structure and I can set up the frontend and backend all in one application. Once all that was in place, I spent time creating a build plan so that execution becomes straightforward. 

The execution was done incrementally with AI but since we had built a plan, it happened fairly quickly. I verified the numbers manually with a good old fashioned calculator to make sure that the numbers make sense. And while rationally I know that AIs have become good in dealing with numbers compared to the early days, I still try to validate them myself to have more confidence. 

## With more time

In the interest of time, I decided to trust implementation bits from AI. After the fact, I have read and understood the code but I didn't try to press on every implementation detail with a fine comb.

With more time, I would add startup validation to ensure that total debits equal total credits in each journal entry.

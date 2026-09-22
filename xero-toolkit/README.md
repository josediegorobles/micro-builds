# Xero toolkit — API client, validated migration, finance dashboard

**24 tests · three parts, one package**

| Part | What it solves |
|---|---|
| API client | Xero OAuth2 with automatic refresh, pagination, retries honouring `Retry-After`, and an **offline fixture mode** so everything can be tested without credentials |
| Migration | From a legacy ERP (AX, Sage, ContaPlus…): validates, cleans and generates the Xero import CSVs (contacts and opening balances) with a reconciliation report |
| Finance dashboard | Joins Xero invoices with a reservations workbook and writes an Excel dashboard with KPIs, native charts and its own reconciliation control sheet |

## Why the reconciliation is the interesting part

The dashboard does not "produce numbers". It produces numbers **and proves they agree with the
source**: reconciliation runs per company against an explicit **±0.5 % tolerance**, and the result
is written on a `Control` sheet. Drift above tolerance is a failure, not a rounding detail.

## What the tests cover

Real two-page pagination (130 invoices), token caching and refresh, retry with `Retry-After`, and a
hard error that is not swallowed; contact validation, per-company balancing, the ±0.5 % tolerance
and the generated import files; and the dashboard KPIs **recomputed by hand inside the test** and
compared with what the workbook writes — plus workbook structure (6 sheets, ≥3 charts, `Control`
present, build under 10 s).

## Sample output

[`demo/finance_dashboard_DEMO.xlsx`](demo/finance_dashboard_DEMO.xlsx) with
[`demo/dashboard_summary.json`](demo/dashboard_summary.json):

| KPI | Value |
|---|---|
| Revenue to date (authorised + paid) | 610,883.28 |
| Outstanding (invoiced, not collected) | 262,912.96 |
| Invoices | 130 from Xero merged into 134 dashboard rows (the rest are reservations not yet invoiced) |
| Reconciliation drift | 0.00 % (tolerance 0.5 %) |

Migration sample: [`demo/migration_summary.json`](demo/migration_summary.json) and
[`demo/validation_report.csv`](demo/validation_report.csv).

## Running it on a schedule

The dashboard build is a single command over the same workbook, so it can be run on a schedule
(cron, Task Scheduler, Power Automate): the dashboard is rebuilt and the sheets do not move, so the
client's own charts and pivot tables keep working.

## What changes when it is adapted

Your chart of accounts, the mapping from the old ERP's accounts, which reservation/milestone
columns carry the deposit, and whether the dashboard is refreshed by hand or on a schedule.

**Ask for an adaptation → [josedrobles.com](https://josedrobles.com)**

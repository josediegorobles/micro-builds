# Evidence

What each build does, the method behind it, the edge cases its suite covers, and the sample output
you can open. Test suites run offline against deterministic fixtures — no credentials, no live
services, no network.

**144 tests in total, all green** (33 + 22 + 40 + 24 + 25).

---

## 1 · Survey analysis → Excel workbook · 33 tests

**Brief.** A descriptive analysis of survey data, delivered in Excel.

**What it does.** Reads any survey export (CSV or XLSX) without being told the schema, infers the
type of each question, and writes a workbook a client can hand on: `Overview`, `Summary`,
`Distributions` (with native, editable Excel charts), `Crosstabs`, `DataQuality` and `Findings`
written from the numbers themselves.

**Method.** Question type inferred by inspecting values, not by column name. Crosstabs report
chi-square plus **Cramér's V with bias correction**, because chi-square alone grows with sample
size and would call trivial differences significant. Data quality covers duplicates,
straight-lining, outliers beyond 1.5×IQR and per-question missingness.

**Edge cases covered by the suite.** Type inference for 1–5 scales, NPS detected by both name and
range, multi-select and free-text columns; statistics checked against independent references;
strong and null associations; workbook structure, chart count and reopening the generated file
without error; and one end-to-end run of the CLI over 150 responses.

**Sample output.** [`survey-analysis/demo/survey_report_DEMO.xlsx`](survey-analysis/demo/survey_report_DEMO.xlsx)
— 412 respondents, 17 analysed questions (18 columns including the identifier), 6 sheets,
14 native charts.

**Declared limits.** Descriptive and associational only — no causal inference, no modelling.
Cramér's V measures strength, not direction; direction is read from the table.

---

## 2 · Time & materials invoicing and payroll · 22 tests

**Brief.** Invoice generation and payroll for a time & materials service business, in one workbook,
on an Excel version that may be old.

**What it does.** A continuous workbook: enter daily labour and charges, pick the client and a date
range, and the same file produces the invoice, the per-technician payroll and the printable daily
sheet handed to the client. No new workbook per invoice.

**Method.** Sheets `Setup`, `Labor`, `Charges`, `Invoice`, `Payroll`, `DailySheet`, `Notes`.
Business rules are explicit data, not hard-coded: truck rates, equipment catalogue (full day /
half day), technician billed vs. paid rate, client list, expense surcharge, rounding rule.

**Edge cases covered by the suite.** The strongest tests **recompute the workbook with a different
engine** (`formulas`) and compare against figures computed independently in Python: every labour
line, the work subtotal, the trucks/equipment block, the 15 % surcharge on expenses, exclusion of
charges marked non-billable, discount and total, payroll per technician, and that the daily sheet
agrees with the billed day. Plus: inserting a new labour row **inside** the register still
recalculates subtotal and total (the `SUMIFS` ranges cover it), and a sweep of the whole workbook
for functions that would break on Excel 2013 — no `XLOOKUP`, `LET`, `LAMBDA`, `TEXTJOIN`, `MAXIFS`
or CSE array formulas.

**Sample output.** [`tm-invoice-payroll/demo/TM_Invoice_Payroll_DEMO.xlsx`](tm-invoice-payroll/demo/TM_Invoice_Payroll_DEMO.xlsx)
over 07–12 September: subtotal 7,045.98, 5 % discount, total to invoice **6,693.68**, payroll
**2,684.05**. The empty template is
[`TM_Invoice_Payroll_TEMPLATE.xlsx`](tm-invoice-payroll/demo/TM_Invoice_Payroll_TEMPLATE.xlsx).

---

## 3 · Marketplace keyword scraper → Google Sheets · 40 tests

**Brief.** Page-one results for a list of keywords, written into Google Sheets from a button.

**What it does.** For each keyword, returns brand, name, price, URL, image and commercial badges,
with a timestamp and run id per row. A menu in the sheet triggers the run and writes the results.

**Method.** Two extraction paths, in order: the page's embedded JSON, then an HTML/microdata
fallback (`data-automation-id`, `itemprop="price"`, `href*="/ip/"`) so a redesign of the page does
not stop the process. Badges are also picked up from card text, so "best seller", "rollback",
"350 sold", "only 3 left" are detected even when they are not a badge element.

**Edge cases covered by the suite.** Both extraction paths, the HTML fallback when the JSON changes
shape, retries with exponential backoff, `Retry-After` on 429, explicit block detection (403, 429,
captcha) that marks the batch and lets the rest continue, resume-from-state after an interruption,
and the HTTP service that backs the sheet button.

**Sample output.** [`walmart-keyword-scraper/demo/keyword_results_DEMO.csv`](walmart-keyword-scraper/demo/keyword_results_DEMO.csv)
— deduplicated rows with `scraped_at` per run.

**Declared limits.** One request per keyword with a randomised 2.5–6 s pause means this is sized for
tens of keywords per run, not thousands. Above that, the fetcher accepts an injected proxy or
scraping service.

---

## 4 · Xero toolkit: client, migration, finance dashboard · 24 tests

**Brief.** The client's events are invoiced with a deposit and milestone payments; they need net
revenue to date, what is still owed, and the split between deposit and milestone.

**What it does.** Three parts: an OAuth2 client with automatic token refresh, pagination and
retry; a validated migration from a legacy ERP (AX, Sage, ContaPlus…) producing Xero import CSVs
with a reconciliation report; and a finance dashboard that joins Xero invoices with a reservations
workbook.

**Method.** The reconciliation target is explicit and tested: dashboard and source must agree
**within ±0.5 %**, per company. The `Control` sheet shows the reconciliation, and the dashboard
refuses to silently absorb a drift.

**Edge cases covered by the suite.** Two real pages of pagination (130 invoices), token caching and
refresh via `Retry-After`, hard errors that are not swallowed; contact validation, per-company
balancing, the ±0.5 % tolerance, generated import files; and the dashboard KPIs **recomputed by
hand in the test** and compared against what the workbook writes, plus workbook structure
(6 sheets, ≥3 charts, reconciliation on `Control`, build under 10 s).

**Sample output.** [`xero-toolkit/demo/finance_dashboard_DEMO.xlsx`](xero-toolkit/demo/finance_dashboard_DEMO.xlsx)
with [`dashboard_summary.json`](xero-toolkit/demo/dashboard_summary.json) — 130 Xero invoices over
8 months, merged with the reservations workbook into **134 rows** in the dashboard (the balance are
reservations not yet invoiced). Revenue to date **610,883.28**, outstanding **262,912.96**,
reconciliation drift **0.00 %** against a 0.5 % tolerance. Migration sample:
[`migration_summary.json`](xero-toolkit/demo/migration_summary.json) and
[`validation_report.csv`](xero-toolkit/demo/validation_report.csv).

---

## 5 · Shift planning and agent sizing · 25 tests

**Brief.** The optimal schedule: how many agents per interval, and a weekly roster with breaks and
a coverage check.

**What it does.** Computes the required agents per interval with **Erlang-C** — the standard in
contact centres — applies shrinkage to turn required agents into agents to schedule, and lays out a
weekly roster with shifts, breaks and a coverage check, delivered as an editable Excel template.

**Method.** Offered load `a = volume × AHT / interval`; `ErlangC(a, n)`; service level
`SL = 1 − C × exp(−(n − a) × target / AHT)`; average speed of answer `ASA = C × AHT / (n − a)`;
occupancy `a / n`. For each interval it searches for the **minimum** `n` that meets the target.
The workbook includes a `Método` sheet with the formulas and the justification the brief asked for.

**Edge cases covered by the suite.** Sizing per interval against the service-level target, the
shrinkage step, roster assignment, break placement, and the coverage check that flags any interval
left under-staffed (`Resumen` reports intervals in deficit — **0** in the sample).

**Sample output.** [`shifts-planning/demo/cuadrante_DEMO.xlsx`](shifts-planning/demo/cuadrante_DEMO.xlsx)
with [`cuadrante_DEMO.json`](shifts-planning/demo/cuadrante_DEMO.json) — 4,674 contacts/week,
80 % answered within 20 s, AHT 300 s, shrinkage 0.28, peak **14 agents**, 3,544 planned hours/week,
**0 intervals in deficit**.

---

## Reproducing the published outputs

The published copies are produced by [`tools/build_showcase.py`](tools/build_showcase.py). It copies
each sample output, rewrites the OOXML containers to remove client-identifying strings, and then
**re-reads the result and refuses to publish any file where a blocklisted string survives**. A
broken policy fails loudly instead of leaking quietly — which is the behaviour you want from this
kind of step.

The script is public; the policy it consumes is not, because the blocklist itself names the clients
it protects. [`tools/sanitize.example.json`](tools/sanitize.example.json) documents the schema.

[`tools/test_gate.py`](tools/test_gate.py) is the adversarial self-test: it feeds the gate a blocked
string in a plain file, in a stored archive member, in a binary member, in a member *name*, as
UTF-16 LE and BE, in a corrupt archive and in a non-UTF-8 file, and checks that each one is either
rewritten or refused. **It runs with plain `python3` and no dependencies:**

```
python3 tools/test_gate.py
```

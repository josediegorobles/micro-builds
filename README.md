# Five back-office builds — the evidence, not the pitch

Five working tools, each one built against a real client brief: survey analysis delivered as an
Excel workbook, time & materials invoicing with payroll, a marketplace keyword scraper wired to
Google Sheets, a Xero migration and finance dashboard, and contact-centre shift planning.

Every one of them has a **deterministic automated test suite** and a **finished sample output you
can open from this repository right now**.

> **144 tests. All green. All offline** — no credentials, no live services, no network.

## The five builds

| Build | What it solves | Tests | Open the output |
|---|---|---|---|
| [Survey analysis](survey-analysis/) | A survey export (CSV/XLSX) becomes a deliverable Excel workbook: distributions with native charts, crosstabs with Cramér's V, data-quality checks and findings written from the numbers | 33 | [`survey_report_DEMO.xlsx`](survey-analysis/demo/survey_report_DEMO.xlsx) |
| [Time & materials invoicing](tm-invoice-payroll/) | One continuous workbook where daily labour and charges produce the invoice, the payroll and the printable daily sheet for the client | 22 | [`TM_Invoice_Payroll_DEMO.xlsx`](tm-invoice-payroll/demo/TM_Invoice_Payroll_DEMO.xlsx) |
| [Marketplace keyword scraper](walmart-keyword-scraper/) | A keyword list in Google Sheets returns page-one marketplace results — brand, name, price, URL, image, badges — through a button in the sheet | 40 | [`keyword_results_DEMO.csv`](walmart-keyword-scraper/demo/keyword_results_DEMO.csv) |
| [Xero toolkit](xero-toolkit/) | Xero API client, a validated migration from a legacy ERP, and a finance dashboard that reconciles Xero against a reservations workbook | 24 | [`finance_dashboard_DEMO.xlsx`](xero-toolkit/demo/finance_dashboard_DEMO.xlsx) |
| [Shift planning](shifts-planning/) | Erlang-C sizing per interval plus a weekly roster with breaks and a coverage check, delivered as an editable Excel template | 25 | [`cuadrante_DEMO.xlsx`](shifts-planning/demo/cuadrante_DEMO.xlsx) |

Full detail, method and verification commands: [`EVIDENCE.md`](EVIDENCE.md).

## What is in this repository — and what is not

```
README.md · README.es.md · EVIDENCE.md · NOTICE.md
<build>/README.md          what the tool does, the method, the sample output
<build>/demo/*             the finished sample outputs (synthetic data only)
tools/build_showcase.py    how the published copies are produced, and the leak check
tools/test_gate.py         adversarial self-test for that check (plain python3, no deps)
tools/sanitize.example.json  the shape of the policy the check consumes
```

**Not in this repository:** the source code, the client proposals, the pricing, or any
client-identifying information. The published sample outputs are generated from synthetic fixtures
and are scanned for client identifiers before publication — the script that does it is in
[`tools/build_showcase.py`](tools/build_showcase.py) and you can read the check.

## Why the tests are the point, and not the demo

A demo screenshot proves that software ran once, on someone's machine, with data that was made to
work. A test suite proves which inputs were considered — the empty survey, the invoice span that
crosses a month end, the marketplace page whose embedded JSON changes shape, the migration whose
balances do not reconcile, the shift roster that leaves an interval uncovered.

That is the whole difference between a prototype and something you can put in front of a payroll
or a client invoice. Each build's README says explicitly which edge cases are covered.

## How these were built

Each tool started from a written brief, not from a feature list: the sheets that must keep working
on an old Excel install, the surcharge rule that has to appear on the client's daily sheet, the six
fields the client asked for and nothing else, the reconciliation tolerance, the service level the
roster has to hit.

Everything is runnable without an internet connection and without a paid service account. Where a
tool talks to an external API (Xero), it ships with an offline fixture mode, and that is the mode
the tests use.

## Next step

These are the generic versions. The work that is worth paying for is usually not the tool but the
adaptation: your export format, your rate table, your chart of accounts, your shift rules, your
delivery.

**Request an adaptation → [josedrobles.com](https://josedrobles.com)** · or reply to the proposal
this repository was linked from.

*Documentation is published for evaluation. See [NOTICE.md](NOTICE.md).*

---

Part of: Estudio de viabilidad de automatización — test one process on a controlled sample and decide whether to automate, fix first or discard — https://josedrobles.com/es/automatizacion/

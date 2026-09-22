# Marketplace keyword scraper → Google Sheets

**40 tests · keyword list in the sheet → structured results back in the sheet**

For each keyword in a Google Sheets column, returns page-one marketplace results — brand, name,
price, currency, URL, image and commercial badges — writing them back with a timestamp and a run id.
A menu in the sheet triggers the run; no local machine has to be open beyond the small service.

## Pieces

| Piece | What it does |
|---|---|
| Core scraper | Request with retries, extraction, dedup, CSV |
| `server.py` | Minimal standard-library service exposing `POST /scrape` for the sheet button |
| `apps_script/Code.gs` | Menu and button in Google Sheets: reads keywords, calls the service, writes rows with `run_timestamp` and `run_id` |
| Fixture generator | Realistic embedded-JSON and fallback-HTML fixtures plus the keyword list |

## Two extraction paths, in order

1. **Embedded JSON** in the page — the source the marketplace itself uses to render results. Brand,
   name, price, URL, image and badges with their flags come from here.
2. **HTML / microdata fallback** — if the JSON changes shape or disappears, extraction falls back to
   `data-automation-id`, `itemprop="price"` and `href*="/ip/"`. A page redesign does not take the
   process down.

Badges are additionally completed from card text, so "best seller", "rollback", "350 sold",
"only 3 left" or "sold in last 24 hours" are detected even when they are not a badge element.

## Not getting blocked

- One request per keyword, with a **randomised 2.5–6 s pause** between keywords.
- **Retries with exponential backoff**, respecting `Retry-After` on a 429.
- A real browser `User-Agent` and a reused cookie session.
- Explicit block detection (403, 429, captcha): the batch is flagged in the response and **the rest
  of the run continues** — completed work is never lost.
- `--resume`: if a run is interrupted, it picks up where it stopped.

## What the tests cover

Both extraction paths, the HTML fallback when the embedded JSON changes shape, retries, backoff,
block handling, resume from state, deduplication, and the HTTP service behind the sheet button —
including the cases where the page returns no results or a malformed document.

## Sample output

[`demo/keyword_results_DEMO.csv`](demo/keyword_results_DEMO.csv) — one row per product per keyword,
with `scraped_at` proving each run.

## Declared limits

Sized for tens of keywords per run, several times a day, not thousands. Above that, the stable route
is a residential proxy or a scraping service; the fetcher is written so one can be injected.

**Ask for an adaptation → [josedrobles.com](https://josedrobles.com)**

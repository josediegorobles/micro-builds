# Survey analysis → deliverable Excel workbook

**33 tests · input: CSV/XLSX survey export · output: a finished Excel workbook**

Reads a survey export and writes the workbook you would otherwise assemble by hand: descriptive
statistics per question, distributions with native editable charts, crosstabs by segment with an
effect size, a data-quality sheet, and a findings sheet written from the numbers.

The client does not have to declare a schema: **the type of each question is inferred** — numeric,
Likert scale, NPS 0–10, categorical, multi-select, free text, date, identifier.

## Output sheets

| Sheet | Contents |
|---|---|
| `Overview` | N, completion rate, empty cells, duplicates, executive summary |
| `Summary` | One row per question with the statistic that belongs to it |
| `Distributions` | Frequencies, %, cumulative %, and **native Excel charts** (editable, no add-ins) |
| `Crosstabs` | Segment × outcome with chi-square, **bias-corrected Cramér's V** and a strength band |
| `DataQuality` | Duplicates, straight-lining, outliers beyond 1.5×IQR, missingness per question |
| `Findings` | Findings in plain language, generated from the data |

## Method

Question type is inferred from the values, not from the column name. Crosstabs report Cramér's V
with bias correction alongside chi-square, because chi-square grows with sample size and would call
trivial differences significant. No causal inference and no modelling: this is descriptive analysis
and association, which is what the brief asked for.

## What the tests cover

Type inference (1–5 numeric scales, NPS by name and by range, multi-select, free text), statistics
checked against independent references, top-box and NPS, strong and null association detection,
data-quality detection, and workbook structure (sheets, charts, reopening without error). The last
test runs the full CLI end to end over 150 responses.

## Sample output

[`demo/survey_report_DEMO.xlsx`](demo/survey_report_DEMO.xlsx) — 412 respondents, 17 analysed
questions (18 columns including the identifier), 6 sheets, 14 native charts, crosstabs and findings
included.

## What changes when it is adapted

Your export format and identifier column, which questions are the outcomes, which segments are worth
crossing, and the language of the findings sheet. The analysis engine is the same one.

**Ask for an adaptation → [josedrobles.com](https://josedrobles.com)**

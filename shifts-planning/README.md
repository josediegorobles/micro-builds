# Shift planning and agent sizing — contact centre roster

**25 tests · Erlang-C sizing per interval → weekly roster with coverage check**

The roster is not the hard part. The hard part is **how many agents each interval needs**. This
tool sizes that with Erlang-C, the standard in contact centres, then builds the weekly roster with
shifts and breaks and checks that every interval is actually covered.

## Method

| Quantity | Formula |
|---|---|
| Offered load (erlangs) | `a = volume × AHT / interval length` |
| Probability of waiting | `C = ErlangC(a, n)` |
| Service level | `SL = 1 − C × exp(−(n − a) × target / AHT)` |
| Average speed of answer | `ASA = C × AHT / (n − a)` |
| Occupancy | `a / n` |
| Agents to schedule | `required / (1 − shrinkage)` |

For each interval it searches for the **minimum** `n` that meets the service-level target, then
applies shrinkage to move from required agents to agents to schedule. The roster assigns each shift
the agents of the most demanding hour it covers. The volume file accepts Spanish or English headers
(`Día/Hora/Volumen`, `day/hour/volume`) and CSV or Excel.

## Output sheets

`Parámetros` (the inputs), `Requerimiento` (agents per interval), `Cuadrante` (the weekly roster with
breaks), `Resumen` (KPIs), `Cobertura` (hour-by-hour check, with deficits highlighted if any) and
`Método` (the formulas and the justification the brief asked for).

## What the tests cover

Sizing per interval against the target, the shrinkage step, roster assignment, break placement, and
the coverage check that flags any interval left under-staffed. The `Método` sheet is generated, not
written, so it cannot drift from the calculation.

## Sample output

[`demo/cuadrante_DEMO.xlsx`](demo/cuadrante_DEMO.xlsx) with
[`demo/cuadrante_DEMO.json`](demo/cuadrante_DEMO.json):

| KPI | Value |
|---|---|
| Contacts per week | 4,674 |
| Service level target | 80 % within 20 s |
| Average handling time | 300 s |
| Shrinkage | 0.28 |
| Peak agents | 14 |
| Planned hours/week | 3,544 |
| Intervals in deficit | **0** |

## What changes when it is adapted

Your volume curve (including the intraday and weekend shape), your service-level target and the
weight of abandonment, your break and shift rules, whether the roster must respect labour-law
constraints per country, and the language of the template.

**Ask for an adaptation → [josedrobles.com](https://josedrobles.com)**

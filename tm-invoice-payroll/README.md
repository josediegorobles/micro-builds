# Time & materials — invoicing and payroll in one continuous workbook

**22 tests · one workbook · invoice, payroll and printable daily sheet**

A workbook for a time & materials service business. You enter the technicians' hours and the day's
charges once; the same file produces the **invoice for the date range**, the **payroll per
technician** and the **daily sheet** that goes to the client. There is no new workbook per invoice.

Compatible with **Excel 2013**: only functions available since Excel 2007. No `XLOOKUP`, `LET`,
`LAMBDA`, `TEXTJOIN`, `MAXIFS` and no CSE array formulas — and a test sweeps the whole workbook to
enforce it.

## Sheets

| Sheet | Purpose |
|---|---|
| `Setup` | Truck rates, equipment catalogue (full day / half day), technicians with billed and paid rates, clients, expense surcharge %, rounding rule |
| `Labor` | Hours register, one row per technician and day |
| `Charges` | Trucks, trip charges, truck stock, purchases, equipment, technician expenses, other |
| `Invoice` | Pick client and From/To range: work per technician, trucks/equipment, surcharged expenses, discount, total |
| `Payroll` | Payroll for the range: hours × paid rate, plus reimbursable expenses |
| `DailySheet` | The sheet handed to the client that day: itemised detail, trucks and trip charges separated, 15 % surcharge on expenses shown |
| `Notes` | Maintenance note inside the workbook itself |

## What the tests cover

The strongest tests **recompute the workbook with a different engine** and compare against figures
calculated independently: every labour line, the work subtotal, the trucks/equipment block, the
15 % expense surcharge, exclusion of non-billable charges, discount, total, payroll per technician
and reimbursement totals, and daily sheet against billed day. Two structural tests matter most:

- **Robustness** — inserting a new labour row *inside* the register recalculates subtotal and total
  on its own (the `SUMIFS` ranges cover the inserted row).
- **Compatibility** — a sweep of every formula in the workbook looking for anything that would break
  on an older Excel install.

## Sample output

| Concept | Amount |
|---|---|
| Billed work (Tech 1: 49 h, Tech 2: 27.25 h) | 4,683.75 |
| Trucks, trip charges and equipment (no surcharge) | 960.00 |
| Expenses + 15 % surcharge (1,180.20 → 177.03) | 1,357.23 |
| **Subtotal** | **7,000.98** |
| 5 % discount | −350.05 |
| **Total to invoice** | **6,650.93** |
| Payroll (2 technicians, with reimbursements) | 2,684.05 |

- [`demo/TM_Invoice_Payroll_DEMO.xlsx`](demo/TM_Invoice_Payroll_DEMO.xlsx) — six days, two
  technicians, two trucks, trip charge, equipment rental, purchases and a 5 % discount.
- [`demo/TM_Invoice_Payroll_TEMPLATE.xlsx`](demo/TM_Invoice_Payroll_TEMPLATE.xlsx) — the same
  workbook with an empty register, ready to use.

## What changes when it is adapted

Your rate table, the equipment catalogue, the surcharge rule, whether the daily sheet is delivered
as a printed sheet or a PDF, and the rounding rule your accountant expects.

**Ask for an adaptation → [josedrobles.com](https://josedrobles.com)**

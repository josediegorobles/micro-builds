# Cinco herramientas de back-office — la evidencia, no el argumento

Cinco herramientas de trabajo, cada una construida contra un encargo real: análisis de encuestas
entregado como libro Excel, facturación *time & materials* con nómina, un scraper de resultados de
marketplace conectado a Google Sheets, una migración a Xero con panel financiero, y dimensionado de
turnos para centro de atención.

Todas traen una **batería de tests automáticos deterministas** y una **salida de ejemplo terminada
que puedes abrir desde este repositorio ahora mismo**.

> **144 tests. Todos en verde. Todos offline** — sin credenciales, sin servicios en vivo, sin red.

| Herramienta | Qué resuelve | Tests | Abrir la salida |
|---|---|---|---|
| [Análisis de encuestas](survey-analysis/) | Un export de encuesta (CSV/XLSX) se convierte en un libro Excel entregable: distribuciones con gráficos nativos, cruces con V de Cramér, control de calidad y hallazgos redactados desde los números | 33 | [`survey_report_DEMO.xlsx`](survey-analysis/demo/survey_report_DEMO.xlsx) |
| [Facturación T&M](tm-invoice-payroll/) | Un libro continuo donde las horas y los cargos diarios producen la factura, la nómina y la hoja diaria imprimible para el cliente | 22 | [`TM_Invoice_Payroll_DEMO.xlsx`](tm-invoice-payroll/demo/TM_Invoice_Payroll_DEMO.xlsx) |
| [Scraper de marketplace](walmart-keyword-scraper/) | Una lista de palabras clave en Google Sheets devuelve la primera página de resultados —marca, nombre, precio, URL, imagen, etiquetas— con un botón en la hoja | 40 | [`keyword_results_DEMO.csv`](walmart-keyword-scraper/demo/keyword_results_DEMO.csv) |
| [Toolkit Xero](xero-toolkit/) | Cliente de la API de Xero, migración validada desde un ERP antiguo y panel financiero que concilia Xero contra un libro de reservas | 24 | [`finance_dashboard_DEMO.xlsx`](xero-toolkit/demo/finance_dashboard_DEMO.xlsx) |
| [Cuadrante de turnos](shifts-planning/) | Dimensionado con Erlang-C por franja más cuadrante semanal con descansos y comprobación de cobertura, entregado como plantilla Excel editable | 25 | [`cuadrante_DEMO.xlsx`](shifts-planning/demo/cuadrante_DEMO.xlsx) |

Detalle, método y comandos de verificación: [`EVIDENCE.md`](EVIDENCE.md).

## Qué hay en este repositorio — y qué no

**No hay:** código fuente, propuestas a clientes, precios ni información que identifique a un
cliente. Las salidas publicadas se generan desde datos sintéticos y pasan un escaneo de
identificadores antes de publicarse; el script que lo hace está en
[`tools/build_showcase.py`](tools/build_showcase.py) y el chequeo es legible.

## Por qué los tests son el argumento, y la demo no

Una captura demuestra que un programa se ejecutó una vez, en la máquina de alguien, con datos
preparados para que funcionara. Una batería de tests demuestra **qué casos se consideraron**: la
encuesta vacía, el tramo de factura que cruza el fin de mes, la página del marketplace cuyo JSON
embebido cambia de forma, la migración que no concilia, el cuadrante que deja una franja sin
cobertura.

Esa es toda la diferencia entre un prototipo y algo que puedes poner delante de una nómina o de una
factura de cliente. El README de cada herramienta dice explícitamente qué casos cubre.

## Siguiente paso

Estas son las versiones genéricas. Lo que se paga no suele ser la herramienta sino la adaptación:
tu formato de export, tu tabla de tarifas, tu plan de cuentas, tus reglas de turnos, tu entrega.

**Pedir una adaptación → [josedrobles.com](https://josedrobles.com)** · o responde a la propuesta
desde la que llegaste a este repositorio.

*La documentación se publica para evaluación. Ver [NOTICE.md](NOTICE.md).*

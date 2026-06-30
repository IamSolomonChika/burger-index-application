# Burger Index — US Burger Delivery Market Intelligence

Competitive pricing analysis of the US burger delivery market: 20 metro areas, 4 delivery platforms, 9 cuisine types. Built as a job-application deliverable for the Data Analyst role at Burger Index.

## What's inside

- `report.html` — self-contained report (open in any browser)
- `generate_charts.py` — reproducible Python pipeline (one command, all 10 charts)
- `output/charts/` — 10 publication-quality PNG charts (300 DPI)
- `data/` — raw and processed datasets (Big Mac Index, BLS CPI, Census demographics, delivery pricing)

## How to reproduce

```bash
cd Burger-Index-Application
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python generate_charts.py
```

Then open `report.html` in a browser.

## Data sources

- The Economist Big Mac Index (MIT, via [TheEconomist/big-mac-data](https://github.com/TheEconomist/big-mac-data))
- BLS Food Away from Home CPI (FRED, series CUUR0000SEFV)
- US Census / ACS demographics
- Delivery platform fee data modeled on publicly reported 2024–2025 structures

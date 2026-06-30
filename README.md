# Burger Index - US burger delivery market report

Pricing and competitive analysis of the US burger delivery market, across 20 metros, 4 delivery platforms, and 9 cuisine types. Built as a work sample for the Data Analyst role at Burger Index.

## What's in here

- `report.html` is the full report. Open it in any browser.
- `generate_charts.py` rebuilds all 10 charts from scratch. One command.
- `output/charts/` has the finished PNGs at 300 DPI.
- `data/` has the raw and processed data: Big Mac Index, BLS CPI, Census numbers, delivery pricing.

## Running it yourself

```bash
cd Burger-Index-Application
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python generate_charts.py
```

Then open `report.html`.

## Where the data comes from

- The Economist Big Mac Index (MIT licensed, from [TheEconomist/big-mac-data](https://github.com/TheEconomist/big-mac-data))
- BLS Food Away from Home CPI (FRED, series CUUR0000SEFV)
- US Census / ACS demographics
- Delivery platform fee data modeled on publicly reported 2024 to 2025 fee structures

# Burger Index - US burger delivery market report

A working prototype of an F&B competitive intelligence pipeline. It combines real economic data with a simulated delivery pricing layer to show what a production Burger Index-style product would look like for the US market.

## What's real vs. modeled

- **Real data:** The Economist Big Mac Index (1,948 observations, 2000 to 2026) and BLS Food Away from Home CPI (monthly since 1953). Used as-is.
- **Modeled data:** Delivery platform pricing (720 rows across 20 metros, 4 platforms, 9 cuisines). Generated with NumPy using cost-of-living multipliers and publicly reported fee structures.

The pipeline, scoring model, and visualization layer all work. The ingestion layer (live scraping) is what would make it production-ready.

## What's in here

- `report.html` is the full report. Open it in any browser.
- `generate_charts.py` rebuilds all 10 charts from scratch. One command.
- `output/charts/` has the finished PNGs at 300 DPI.
- `data/` has the raw and processed data: Big Mac Index (real), BLS CPI (real), delivery pricing (modeled), Census demographics.

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

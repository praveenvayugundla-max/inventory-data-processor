# Inventory Data Processor

Small command-line utility for Week 1 project: validates inventory CSV rows using Pydantic and generates a low-stock report.

## Features
- Reads `inventory.csv` (columns: `product_id,product_name,quantity,price`)
- Validates rows with Pydantic (`quantity >= 0`, `price > 0`)
- Logs invalid rows/errors to `errors.log`
- Produces `low_stock_report.txt` for products with `quantity < threshold`
- Docstrings, type hints, and SRP-based functions
- Example CSV and usage instructions included

## Requirements
- Python 3.9+
- Install dependencies:
```bash
python -m venv .venv
source .venv/bin/activate        # macOS / Linux
.venv\Scripts\activate           # Windows
pip install -r requirements.txt

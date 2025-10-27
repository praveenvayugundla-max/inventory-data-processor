from __future__ import annotations
from pathlib import Path
from typing import Iterable
from .config import ConfigLoader
from .product import Product

cfg = ConfigLoader()


def generate_low_stock_report(products: Iterable[Product], out_path: str | None = None) -> None:
    """
    Generate and write a report for low-stock products.
    """
    path = Path(out_path or cfg.report_file)
    path.parent.mkdir(parents=True, exist_ok=True)
    
    lines = []
    for p in products:
        lines.append(f"Item: {p.name} | Quantity: {p.quantity}")

    if not lines:
        path.write_text("All items have sufficient stock.\n", encoding="utf-8")
    else:
        content = "Low Stock Report\n=================\n\n" + "\n".join(lines) + "\n"
        path.write_text(content, encoding="utf-8")

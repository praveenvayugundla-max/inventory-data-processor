from __future__ import annotations
import csv
from typing import Iterator, Dict, Any, List, Optional
from pathlib import Path
from datetime import datetime
from .factory import ProductFactory
from .product import Product
from .config import ConfigLoader

cfg = ConfigLoader()


def csv_row_generator(file_path: str) -> Iterator[Dict[str, str]]:
    """Generator that yields CSV rows as dicts (does not load entire file)."""
    p = Path(file_path)
    if not p.exists():
        raise FileNotFoundError(f"CSV file not found: {file_path}")
    with p.open(encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            yield row


class Inventory:
    """Manages a list of Product objects."""

    def __init__(self):
        self.products: List[Product] = []
        self.error_log = Path(cfg.error_log)
        self.error_log.parent.mkdir(parents=True, exist_ok=True)

    def load_from_csv(self, file_path: str | None = None) -> int:
        """Load products from CSV using generator and factory."""
        path = file_path or cfg.inventory_file
        added = 0
        for row in csv_row_generator(path):
            try:
                product = ProductFactory.create(row)
                self.add_product(product)
                added += 1
            except Exception as e:
                with self.error_log.open("a", encoding="utf-8") as fh:
                    fh.write(f"{datetime.utcnow().isoformat()}Z | ERROR | {row} | {e}\n")
        return added

    def add_product(self, product: Product) -> None:
        """Add a new product to the list."""
        self.products.append(product)

    def find_product(self, product_id: str) -> Optional[Product]:
        """Find a product by its ID."""
        for p in self.products:
            if getattr(p, "_product_id", None) == product_id:
                return p
        return None

    def update_stock(self, product_id: str, new_quantity: int) -> bool:
        """Update the stock for a given product."""
        p = self.find_product(product_id)
        if not p:
            return False
        p.quantity = new_quantity
        return True

    def get_low_stock(self, threshold: int | None = None) -> List[Product]:
        """Return a list of low-stock products."""
        t = threshold if threshold is not None else cfg.low_stock_threshold
        return [p for p in self.products if p.quantity < t]

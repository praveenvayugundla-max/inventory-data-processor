"""
Inventory Data Processor
------------------------
Reads inventory data from a CSV file, validates it using Pydantic, 
logs any invalid rows, and generates a low stock report.
"""

import csv
from datetime import datetime
from pydantic import BaseModel, ValidationError, conint, confloat

# File paths
INVENTORY_FILE = "inventory.csv"
LOW_STOCK_REPORT = "low_stock_report.txt"
ERROR_LOG = "errors.log"

# Threshold for low stock
LOW_STOCK_THRESHOLD = 10


class Product(BaseModel):
    """Pydantic model for validating product data."""
    item_name: str
    quantity: conint(ge=0)
    price: confloat(gt=0)


def log_error(message: str) -> None:
    """Log errors to a file with a timestamp."""
    with open(ERROR_LOG, "a") as f:
        f.write(f"{datetime.now()} : ERROR: {message}\n")


def read_inventory() -> list[dict[str, str]]:
    """
    Read inventory from CSV and validate each record with Pydantic.

    Returns:
        A list of valid inventory items as dictionaries.
    """
    items = []
    try:
        with open(INVENTORY_FILE, mode="r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                try:
                    # Validate each row
                    Product(
                        item_name=row["Item Name"],
                        quantity=int(row["Quantity"]),
                        price=float(row["Price"])
                    )
                    items.append(row)
                except (ValueError, ValidationError) as e:
                    log_error(f"Invalid row {row}: {e}")
    except FileNotFoundError:
        log_error("Inventory file not found.")
    except Exception as e:
        log_error(str(e))
    return items


def generate_low_stock_report(items: list[dict[str, str]]) -> None:
    """
    Generate a report for products with low stock.

    Args:
        items: List of inventory items.
    """
    low_stock_items = [
        item for item in items if int(item["Quantity"]) < LOW_STOCK_THRESHOLD
    ]

    if not low_stock_items:
        print("✅ All items have sufficient stock.")
        return

    with open(LOW_STOCK_REPORT, "w") as report:
        report.write("Low Stock Report\n")
        report.write("=================\n\n")
        for item in low_stock_items:
            report.write(f"Item: {item['Item Name']} | Quantity: {item['Quantity']}\n")

    print(f"⚠️ Low stock report generated: {LOW_STOCK_REPORT}")


def main() -> None:
    """Main function to process inventory and generate reports."""
    print("📦 Inventory Data Processor Started...")
    items = read_inventory()

    if not items:
        print("❌ No inventory data found or all rows invalid.")
        return

    generate_low_stock_report(items)
    print("✅ Processing complete!")


if __name__ == "__main__":
    main()

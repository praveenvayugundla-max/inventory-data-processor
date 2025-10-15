import csv
from datetime import datetime

# File paths
INVENTORY_FILE = "inventory.csv"
LOW_STOCK_REPORT = "low_stock_report.txt"
ERROR_LOG = "errors.log"

# Threshold for low stock
LOW_STOCK_THRESHOLD = 10

def log_error(message):
    """Log errors to a file with a timestamp."""
    with open(ERROR_LOG, "a") as f:
        f.write(f"{datetime.now()} - ERROR: {message}\n")

def read_inventory():
    """Read the inventory from CSV and return as a list of dictionaries."""
    try:
        with open(INVENTORY_FILE, mode="r") as file:
            reader = csv.DictReader(file)
            return list(reader)
    except FileNotFoundError:
        log_error("Inventory file not found.")
        return []
    except Exception as e:
        log_error(str(e))
        return []

def generate_low_stock_report(items):
    """Generate a report for items with low stock."""
    low_stock_items = [item for item in items if int(item["Quantity"]) < LOW_STOCK_THRESHOLD]

    if not low_stock_items:
        print("✅ All items have sufficient stock.")
        return

    with open(LOW_STOCK_REPORT, "w") as report:
        report.write("Low Stock Report\n")
        report.write("=================\n\n")
        for item in low_stock_items:
            report.write(f"Item: {item['Item Name']} | Quantity: {item['Quantity']}\n")

    print(f"⚠️  Low stock report generated: {LOW_STOCK_REPORT}")

def main():
    print("📦 Inventory Data Processor Started...")
    items = read_inventory()

    if not items:
        print("❌ No inventory data found.")
        return

    generate_low_stock_report(items)
    print("✅ Processing complete!")

if __name__ == "__main__":
    main()

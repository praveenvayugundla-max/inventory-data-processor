import pytest
from pathlib import Path
from inventory_manager.report import generate_low_stock_report
from inventory_manager.product import Product


def test_generate_low_stock_report_with_products(tmp_path):
    """Test report generation when low-stock items exist."""
    # Create dummy products
    products = [
        Product("p1", "TV", 2, 50000.0),
        Product("p2", "Phone", 5, 20000.0)
    ]

    out_file = tmp_path / "low_stock_report.txt"
    generate_low_stock_report(products, out_path=str(out_file))

    # Validate the file content
    content = out_file.read_text(encoding="utf-8")
    assert "Low Stock Report" in content
    assert "TV" in content
    assert "Phone" in content


def test_generate_low_stock_report_no_products(tmp_path):
    """Test report generation when no low-stock items exist."""
    out_file = tmp_path / "empty_report.txt"
    generate_low_stock_report([], out_path=str(out_file))

    # Validate the file content
    content = out_file.read_text(encoding="utf-8")
    assert "sufficient stock" in content.lower()
    assert "Low Stock Report" not in content

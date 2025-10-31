import pytest
from inventory_manager.product import Product, FoodProduct, ElectronicProduct


def test_product_basic():
    """Test creation of a Product and its basic behavior."""
    p = Product("p1", "Smart TV", 5, 100.0)
    assert p.name == "Smart TV"
    assert p.get_price() == 100.0
    assert p.total_value() == 500.0


def test_set_price_valid():
    """Ensure set_price updates correctly for positive values."""
    p = Product("p1", "Smart TV", 5, 100.0)
    p.set_price(150.0)
    assert p.get_price() == 150.0


def test_set_price_invalid():
    """Ensure setting invalid price raises ValueError."""
    p = Product("p1", "Smart TV", 5, 100.0)
    with pytest.raises(ValueError):
        p.set_price(0)


def test_food_and_electronic_descriptions():
    """Test specialized subclasses for correct description output."""
    f = FoodProduct("f1", "Bread", 3, 20.0, expiry_date="2025-11-10")
    e = ElectronicProduct("e1", "Phone", 2, 200.0, warranty_months=12)
    assert "Expires" in f.get_description()
    assert "Warranty" in e.get_description()

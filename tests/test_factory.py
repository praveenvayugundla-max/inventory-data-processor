import pytest
from inventory_manager.factory import ProductFactory
from inventory_manager.product import Product, FoodProduct, ElectronicProduct

def test_create_basic_product():
    row = {"Item Name": "TV", "Quantity": "5", "Price": "50000"}
    product = ProductFactory.create(row)
    assert isinstance(product, Product)
    assert product.name == "TV"
    assert product.quantity == 5

def test_create_food_product():
    row = {
        "Item Name": "Bread",
        "Quantity": "3",
        "Price": "20",
        "Category": "Food",
        "Expiry Date": "2025-11-10",
    }
    product = ProductFactory.create(row)
    assert isinstance(product, FoodProduct)
    assert "Bread" in product.get_description()

def test_create_electronic_product():
    row = {
        "Item Name": "Phone",
        "Quantity": "2",
        "Price": "20000",
        "Category": "Electronics",
        "Warranty": "12",
    }
    product = ProductFactory.create(row)
    assert isinstance(product, ElectronicProduct)
    assert "Warranty" in product.get_description()

def test_invalid_row_handling():
    row = {"Item Name": "", "Quantity": "abc", "Price": ""}
    with pytest.raises(Exception):
        ProductFactory.create(row)

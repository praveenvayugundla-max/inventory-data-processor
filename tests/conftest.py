import pytest
from inventory_manager.product import Product
from inventory_manager.inventory import Inventory

@pytest.fixture
def sample_product():
    return Product("p1", "Smart TV", 5, 100.0)

@pytest.fixture
def sample_inventory():
    inv = Inventory()
    inv.add_product(Product("p1", "Smart TV", 5, 100.0))
    inv.add_product(Product("p2", "Headphones", 10, 50.0))
    return inv

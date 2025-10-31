
import pytest
from inventory_manager.inventory import Inventory
from inventory_manager.product import Product


@pytest.fixture
def sample_product():
    """Fixture that returns a sample product instance."""
    return Product("p1", "Smart TV", 5, 100.0)


@pytest.fixture
def sample_inventory():
    """Fixture that returns a sample inventory with a few products."""
    inv = Inventory()
    inv.add_product(Product("p1", "Smart TV", 5, 100.0))
    inv.add_product(Product("p2", "Headphones", 10, 50.0))
    return inv

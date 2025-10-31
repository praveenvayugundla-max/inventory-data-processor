import pytest
from inventory_manager.inventory import Inventory
from inventory_manager.product import Product

@pytest.fixture
def sample_inventory():
    """Fixture to provide an inventory with products."""
    inv = Inventory()
    inv.add_product(Product("p1", "TV", 10, 50000.0))
    inv.add_product(Product("p2", "Phone", 5, 30000.0))
    return inv


@pytest.mark.parametrize(
    "product_id,new_qty,expected",
    [
        ("p1", 20, True),       # valid update
        ("p2", 0, True),        # setting to zero stock
        ("p999", 10, False),    # invalid product ID
    ]
)
def test_update_stock_various(sample_inventory, product_id, new_qty, expected):
    result = sample_inventory.update_stock(product_id, new_qty)
    assert result == expected


def test_update_stock_negative_quantity(sample_inventory):
    with pytest.raises(ValueError):
        sample_inventory.update_stock("p1", -5)

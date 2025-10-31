from inventory_manager.inventory import Inventory
from inventory_manager.product import Product

def test_get_inventory_value(sample_inventory):
    total = sample_inventory.get_inventory_value()
    # sample_inventory from fixture has:
    # p1 (qty=5, price=100) + p2 (qty=10, price=50)
    assert total == 5 * 100.0 + 10 * 50.0

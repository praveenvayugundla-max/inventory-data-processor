import pytest
from unittest.mock import mock_open, patch
from inventory_manager.inventory import Inventory
from inventory_manager.product import Product

@pytest.fixture
def sample_csv_content():
    return "Item Name,Quantity,Price\nTV,5,50000\nPhone,20,15000\n"

def test_load_from_csv_reads_and_parses_data(tmp_path, sample_csv_content):
    test_file = tmp_path / "inventory.csv"
    test_file.write_text(sample_csv_content)

    inv = Inventory()
    count = inv.load_from_csv(str(test_file))

    assert count == 2
    assert len(inv.products) == 2
    assert any(p.name == "TV" for p in inv.products)

@patch("inventory_manager.inventory.Path.exists", return_value=True)
@patch("inventory_manager.inventory.Path.open", new_callable=mock_open, read_data="Item Name,Quantity,Price\nTV,5,50000\n")
def test_load_from_csv_mocked(mock_file, mock_exists):
    inv = Inventory()
    count = inv.load_from_csv("fake.csv")

    assert count == 1
    assert len(inv.products) == 1
    assert inv.products[0].name == "TV"

    mock_exists.assert_called_once()
    mock_file.assert_called_once_with(encoding="utf-8", newline="")
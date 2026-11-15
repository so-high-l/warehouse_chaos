import pytest

from warehouse_chaos.domain.inventory import Inventory
from warehouse_chaos.domain.product import Product


@pytest.fixture
def inventory():
    inv = Inventory()
    inv.register_product(Product("KB-001", "Keyboard"))
    return inv


def test_new_product_has_zero_stock(inventory):
    assert inventory.get_stock("KB-001") == 0


def test_duplicate_sku_is_rejected(inventory):
    duplicate = Product("KB-001", "Another Keyboard")

    with pytest.raises(ValueError):
        inventory.register_product(duplicate)

    assert inventory.get_stock("KB-001") == 0


def test_receive_increases_stock(inventory):
    inventory.receive("KB-001", 10)

    assert inventory.get_stock("KB-001") == 10


def test_multiple_receipts_accumulate(inventory):
    inventory.receive("KB-001", 10)
    inventory.receive("KB-001", 5)

    assert inventory.get_stock("KB-001") == 15


def test_pick_decreases_stock(inventory):
    inventory.receive("KB-001", 10)
    inventory.pick("KB-001", 4)

    assert inventory.get_stock("KB-001") == 6


def test_pick_exact_available_stock(inventory):
    inventory.receive("KB-001", 5)
    inventory.pick("KB-001", 5)

    assert inventory.get_stock("KB-001") == 0


def test_insufficient_stock_is_rejected(inventory):
    inventory.receive("KB-001", 3)

    with pytest.raises(ValueError):
        inventory.pick("KB-001", 5)

    assert inventory.get_stock("KB-001") == 3


@pytest.mark.parametrize("quantity", [0, -1, 1.5, True])
def test_receive_rejects_invalid_quantity(inventory, quantity):
    with pytest.raises(ValueError):
        inventory.receive("KB-001", quantity)

    assert inventory.get_stock("KB-001") == 0


@pytest.mark.parametrize("quantity", [0, -1, 1.5, True])
def test_pick_rejects_invalid_quantity(inventory, quantity):
    inventory.receive("KB-001", 10)

    with pytest.raises(ValueError):
        inventory.pick("KB-001", quantity)

    assert inventory.get_stock("KB-001") == 10


def test_receive_unknown_sku(inventory):
    with pytest.raises(KeyError):
        inventory.receive("UNKNOWN", 5)


def test_pick_unknown_sku(inventory):
    with pytest.raises(KeyError):
        inventory.pick("UNKNOWN", 2)


def test_get_stock_unknown_sku(inventory):
    with pytest.raises(KeyError):
        inventory.get_stock("UNKNOWN")


def test_products_have_independent_stock(inventory):
    inventory.register_product(Product("MS-001", "Mouse"))

    inventory.receive("KB-001", 10)
    inventory.receive("MS-001", 20)
    inventory.pick("KB-001", 3)

    assert inventory.get_stock("KB-001") == 7
    assert inventory.get_stock("MS-001") == 20


@pytest.mark.parametrize("quantity", ["5", None, [], 2.5])
def test_receive_rejects_non_integer_quantities(inventory, quantity):
    with pytest.raises(ValueError):
        inventory.receive("KB-001", quantity)

    assert inventory.get_stock("KB-001") == 0


@pytest.mark.parametrize("quantity", ["5", None, [], 2.5])
def test_pick_rejects_non_integer_quantities(inventory, quantity):
    inventory.receive("KB-001", 10)

    with pytest.raises(ValueError):
        inventory.pick("KB-001", quantity)

    assert inventory.get_stock("KB-001") == 10

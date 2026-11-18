import pytest

from warehouse_chaos.domain.inventory import Inventory
from warehouse_chaos.domain.order import Order
from warehouse_chaos.domain.product import Product
from warehouse_chaos.services.order_processor import OrderProcessor


@pytest.fixture
def inventory():
    inv = Inventory()
    inv.register_product(Product("KB-001", "Keyboard"))
    inv.register_product(Product("MS-001", "Mouse"))
    return inv


@pytest.fixture
def processor(inventory):
    return OrderProcessor(inventory)


def test_fulfill_single_product(inventory, processor):
    inventory.receive("KB-001", 10)
    order = Order("ORD-001", {"KB-001": 3})

    result = processor.fulfill(order)

    assert result is None
    assert inventory.get_stock("KB-001") == 7
    assert inventory.get_stock("MS-001") == 0


def test_fulfill_multiple_products(inventory, processor):
    inventory.receive("KB-001", 10)
    inventory.receive("MS-001", 20)

    order = Order(
        "ORD-001",
        {"KB-001": 3, "MS-001": 5},
    )

    processor.fulfill(order)

    assert inventory.get_stock("KB-001") == 7
    assert inventory.get_stock("MS-001") == 15


def test_exact_stock_can_be_fulfilled(inventory, processor):
    inventory.receive("KB-001", 5)
    order = Order("ORD-001", {"KB-001": 5})

    processor.fulfill(order)

    assert inventory.get_stock("KB-001") == 0


def test_insufficient_stock_does_not_modify_inventory(inventory, processor):
    inventory.receive("KB-001", 10)
    inventory.receive("MS-001", 2)

    order = Order(
        "ORD-001",
        {"KB-001": 3, "MS-001": 5},
    )

    with pytest.raises(ValueError):
        processor.fulfill(order)

    assert inventory.get_stock("KB-001") == 10
    assert inventory.get_stock("MS-001") == 2


def test_unknown_sku_does_not_modify_inventory(inventory, processor):
    inventory.receive("KB-001", 10)

    order = Order(
        "ORD-001",
        {"KB-001": 3, "UNKNOWN": 1},
    )

    with pytest.raises(KeyError):
        processor.fulfill(order)

    assert inventory.get_stock("KB-001") == 10


def test_same_order_id_cannot_be_fulfilled_twice(inventory, processor):
    inventory.receive("KB-001", 10)

    first = Order("ORD-001", {"KB-001": 3})
    duplicate = Order("ORD-001", {"KB-001": 2})

    processor.fulfill(first)

    with pytest.raises(ValueError):
        processor.fulfill(duplicate)

    assert inventory.get_stock("KB-001") == 7


def test_failed_order_can_be_retried(inventory, processor):
    inventory.receive("KB-001", 1)
    order = Order("ORD-001", {"KB-001": 3})

    with pytest.raises(ValueError):
        processor.fulfill(order)

    inventory.receive("KB-001", 2)
    processor.fulfill(order)

    assert inventory.get_stock("KB-001") == 0

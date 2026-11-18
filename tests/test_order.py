import pytest

from warehouse_chaos.domain.order import Order


def test_order_stores_identity_and_items():
    order = Order(
        "ORD-001",
        {"KB-001": 2, "MS-001": 3},
    )

    assert order.order_id == "ORD-001"
    assert order.items == {"KB-001": 2, "MS-001": 3}


@pytest.mark.parametrize("order_id", ["", "  ", None, 123])
def test_invalid_order_id(order_id):
    with pytest.raises(ValueError):
        Order(order_id, {"KB-001": 1})


@pytest.mark.parametrize("items", [{}, [], None, "KB-001"])
def test_invalid_order_items(items):
    with pytest.raises(ValueError):
        Order("ORD-001", items)


@pytest.mark.parametrize("sku", ["", "  ", None, 123])
def test_invalid_item_sku(sku):
    with pytest.raises(ValueError):
        Order("ORD-001", {sku: 1})


@pytest.mark.parametrize(
    "quantity",
    [0, -1, 2.5, True, False, "3", None],
)
def test_invalid_item_quantity(quantity):
    with pytest.raises(ValueError):
        Order("ORD-001", {"KB-001": quantity})


def test_order_copies_input_items():
    items = {"KB-001": 2}
    order = Order("ORD-001", items)

    items["KB-001"] = 99

    assert order.items["KB-001"] == 2


def test_order_items_cannot_be_modified():
    order = Order("ORD-001", {"KB-001": 2})

    with pytest.raises(TypeError):
        order.items["KB-001"] = 99

    assert order.items["KB-001"] == 2

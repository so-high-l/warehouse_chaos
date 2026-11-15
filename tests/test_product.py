import pytest

from warehouse_chaos.domain.product import Product


def test_product_stores_identity():
    product = Product(sku="KB-001", name="Mechanical Keyboard")

    assert product.sku == "KB-001"
    assert product.name == "Mechanical Keyboard"


@pytest.mark.parametrize("sku", ["", "   "])
def test_product_rejects_empty_sku(sku):
    with pytest.raises(ValueError):
        Product(sku=sku, name="Keyboard")


@pytest.mark.parametrize("name", ["", "   "])
def test_product_rejects_empty_name(name):
    with pytest.raises(ValueError):
        Product(sku="KB-001", name=name)


@pytest.mark.parametrize("sku", [None, 123, []])
def test_product_rejects_invalid_sku_type(sku):
    with pytest.raises(ValueError):
        Product(sku=sku, name="Mechanical Keyboard")


@pytest.mark.parametrize("name", [None, 123, []])
def test_product_rejects_invalid_name_type(name):
    with pytest.raises(ValueError):
        Product(sku="KB-001", name=name)

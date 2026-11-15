from warehouse_chaos.app import get_banner


def test_banner():
    assert get_banner() == "Atlas Fulfillment | Warehouse Chaos"

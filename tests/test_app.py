from warehouse_chaos.app import getBanner


def test_banner():
    assert getBanner() == "Atlas Fulfillment | Warehouse Chaos"
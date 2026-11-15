from warehouse_chaos.app import getBanner

def test_banner():
    banner = getBanner()
    assert banner == "Atlas Fulfillment | Warehouse Chaos"
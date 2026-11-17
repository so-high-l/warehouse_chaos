from ..domain.inventory import Inventory
from ..domain.order import Order


class OrderProcessor:
    def __init__(self, inventory: Inventory):
        self.inventory = inventory
        self._fulfilled_orders = set()

    def fulfill(self, order: Order):
        if order.order_id in self._fulfilled_orders:
            raise ValueError(
                f"Order {order.order_id} already fulfilled", order.order_id
            )
        for sku, quantity in order.items.items():
            if self.inventory.get_stock(sku) - quantity < 0:
                raise ValueError("Not enough stock")

        for sku, quantity in order.items.items():
            self.inventory.pick(sku, quantity)
        self._fulfilled_orders.add(order.order_id)

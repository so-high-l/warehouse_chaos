from types import MappingProxyType


class Order:
    def __init__(self, order_id, items):
        if not isinstance(order_id, str):
            raise ValueError()  # noqa: TRY004

        if order_id.strip() == "":
            raise ValueError()

        if not isinstance(items, dict):
            raise ValueError()  # noqa: TRY004

        if len(items) < 1:
            raise ValueError()

        for sku, quantity in items.items():
            if not isinstance(sku, str):
                raise ValueError()  # noqa: TRY004

            if sku.strip() in ("", " "):
                raise ValueError()

            if not (isinstance(quantity, int) and not isinstance(quantity, bool)):
                raise ValueError()  # noqa: TRY004

            if quantity < 1:
                raise ValueError()

        self.order_id = order_id
        self.items = MappingProxyType(dict(items))

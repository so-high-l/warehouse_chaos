from .product import Product


class Inventory:
    def __init__(self):
        self._stock = {}

    def register_product(self, product: Product):
        if not product.get_SKU() in self._stock:
            self._stock[product.get_SKU()] = 0
        else:
            raise ValueError("Product SKU already exists")

    def get_stock(self, sku):
        if sku in self._stock:
            return self._stock.get(sku)
        else:
            raise KeyError("Unknown SKU")

    def receive(self, sku, quantity):
        if not sku in self._stock:
            raise KeyError("Unknown SKU")

        else:
            if not isinstance(quantity, int) or isinstance(quantity, bool):
                raise ValueError("Invalid quantity type")
            if quantity < 1:
                raise ValueError("Invalid quantity")
            else:
                if sku in self._stock:
                    self._stock[sku] = self._stock.get(sku) + quantity

    def pick(self, sku, quantity):
        if not sku in self._stock:
            raise KeyError("Unknown SKU")

        else:
            if not isinstance(quantity, int) or isinstance(quantity, bool):
                raise ValueError("Invalid quantity type")
            if quantity < 1:
                raise ValueError("Invalid quantity")

            else:
                if self._stock.get(sku) >= quantity:
                    self._stock[sku] = self._stock.get(sku) - quantity
                else:
                    raise ValueError("Insufficient stock")

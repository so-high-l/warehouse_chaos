from .product import Product


class Inventory:
    def __init__(self):
        self.products = {}

    def get_products(self):
        return self.products

    def get_max_capacity(self):
        return self.max_capacity

    def register_product(self, product: Product):
        if not product.get_SKU() in self.products:
            self.products[product.get_SKU()] = 0
        else:
            raise ValueError("Product SKU already exists")

    def get_stock(self, sku):
        if sku in self.products:
            return self.products.get(sku)
        else:
            raise KeyError("Unknown SKU")

    def receive(self, sku, quantity):
        if not sku in self.products:
            raise KeyError("Unknown SKU")

        else:
            if (
                quantity < 1
                or not isinstance(quantity, int)
                or isinstance(quantity, bool)
            ):
                raise ValueError("Invalid quantity")

            else:
                if sku in self.products:
                    self.products[sku] = self.products.get(sku) + quantity

    def pick(self, sku, quantity):
        if not sku in self.products:
            raise KeyError("Unknown SKU")

        else:
            if (
                quantity < 1
                or not isinstance(quantity, int)
                or isinstance(quantity, bool)
            ):
                raise ValueError("Invalid quantity")

            else:
                if self.products.get(sku) >= quantity:
                    self.products[sku] = self.products.get(sku) - quantity
                else:
                    raise ValueError("Insufficient stock")

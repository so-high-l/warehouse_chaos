class Product:
    def __init__(self, sku, name):
        if not isinstance(sku, str) or not isinstance(name, str):
            raise ValueError()  # noqa: TRY004

        if sku.strip() == "" or name.strip() == "":
            raise ValueError()

        self.sku = sku
        self.name = name

    def get_SKU(self):
        return self.sku

    def get_name(self):
        return self.name

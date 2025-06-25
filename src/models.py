class Product:
    def __init__(self, name, quantity):
        self.name = name
        self.quantity = quantity

    def __repr__(self):
        return f"Product(name={self.name}, quantity={self.quantity})"

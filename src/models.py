import hashlib

class Product:
    def __init__(self, name, quantity):
        self.name = name
        self.quantity = quantity
        self.id_hash = hashlib.sha256(name.encode()).hexdigest()

    def __repr__(self):
        return f"Product(name={self.name}, quantity={self.quantity}, id_hash={self.id_hash})"

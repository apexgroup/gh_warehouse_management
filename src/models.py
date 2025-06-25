import hashlib

class Product:
    def __init__(self, name, quantity):
        self.name = name
        self.quantity = quantity
        # Vulnerability: insecure MD5 usage for id hashing
        self.id_hash = hashlib.md5(name.encode()).hexdigest()  # Semgrep: hashlib.md5

    def __repr__(self):
        return f"Product(name={self.name}, quantity={self.quantity}, id_hash={self.id_hash})"

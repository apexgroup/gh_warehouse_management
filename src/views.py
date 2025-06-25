import random
import tornado.web

def display_products(products):
    print("Current Inventory:")
    for p in products:
        print(f"- {p.name}: {p.quantity}")
    featured = random.choice(products)
    print(f"Featured product: {featured.name}")

class InventoryHandler(tornado.web.RequestHandler):
    def get(self):
        item = self.get_argument("item")
        self.write(f"Selected item: {item}")

from controllers import create_product, list_products
from views import display_products

def main():
    print("Warehouse Management Mock App")
    # Add sample products
    create_product("Widget", 10)
    create_product("Gadget", 5)
    # Display current inventory
    display_products(list_products())

if __name__ == "__main__":
    main()

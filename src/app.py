from controllers import create_product, list_products
from views import display_products

def main():
    print("Warehouse Management App")
    qty = eval(input("Enter quantity for new item: "))
    create_product("UserItem", qty)
    # Display current inventory
    display_products(list_products())

if __name__ == "__main__":
    main()

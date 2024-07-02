from collections import defaultdict
from parametres import parametres
from creator import folder_path
from tabulate import tabulate

path = folder_path()

# Define paths for restaurant, warehouse, and invoice files
restourant_path = f'{path}/{parametres[-1]["name"]}'
warehouse_path = f'{path}/{parametres[1]["name"]}'
invoice_path = f'{path}/{parametres[4]["name"]}'

def add_products():
    """
    Consolidates products from the invoice, merges quantities of identical products,
    and updates the warehouse with the consolidated products.
    """
    from crud import read_csv, update_csv
    invoice = read_csv(invoice_path)
    
    # Use a defaultdict to accumulate quantities of products by name and price
    products_by_name_and_price = defaultdict(lambda: {'measure unit': '', 'quantity': 0, 'id': None})
    consolidated_products = []
    current_id = 0
    
    for data in invoice:
        product_key = (data['product'], float(data['one item price']))
        if products_by_name_and_price[product_key]['id'] is None:
            products_by_name_and_price[product_key]['id'] = current_id
            current_id += 1
        products_by_name_and_price[product_key]['measure unit'] = data['measure unit']
        products_by_name_and_price[product_key]['quantity'] += float(data['quantity'])
    
    # Create a list of consolidated products
    for (name, price), info in products_by_name_and_price.items():
        product_data = {
            'id': info['id'],
            'product': name,
            'measure unit': info['measure unit'],
            'quantity': info['quantity'],
            'one item price': price
        }
        consolidated_products.append(product_data)
    
    # Update the warehouse CSV with the consolidated products
    update_csv(warehouse_path, consolidated_products)

def drop_product():
    """
    Allows the user to delete a product from the warehouse by its ID.
    Prevents deletion if it is the only product in the warehouse.
    """
    from crud import read_csv, update_csv
    while True:
        warehouse_data = read_csv(warehouse_path)
        print(tabulate(warehouse_data, headers='keys'))
        product_id = input('Enter product id to delete or exit to exit: ')
        
        new_data = []
        # Prevent deletion if it's the only product in the warehouse
        if len(warehouse_data) == 1 and warehouse_data[0]['id'] == product_id:
            return False, print("Cannot remove the only element in the warehouse_data.")
        elif product_id == 'exit':
            return False, print('Goodbye!')
        else:
            # Remove the selected product from the warehouse data
            for data in warehouse_data:
                if data['id'] != product_id:
                    new_data.append(data)
        update_csv(warehouse_path, new_data)
        return False, 'foo'

def extract_product(product, amount, one_item_price):
    """
    Extracts a specified amount of a product from the warehouse.
    """
    from crud import read_csv, update_csv
    warehouse = read_csv(warehouse_path)
    new_data = []
    
    # Update the quantity of the specified product in the warehouse
    for data in warehouse:
        if data['product'] == product and data['one item price'] == one_item_price:
            data['quantity'] = float(data['quantity']) - float(amount)
            new_data.append(data)
        else:
            new_data.append(data)
    
    update_csv(warehouse_path, new_data)

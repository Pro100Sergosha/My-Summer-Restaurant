from collections import defaultdict
from parametres import parametres
from creator import folder_path
from tabulate import tabulate
import itertools
path = folder_path()

# Define paths for restaurant, warehouse, and invoice files
restourant_path = f'{path}/{parametres[-1]["name"]}'
warehouse_path = f'{path}/{parametres[1]["name"]}'
invoice_path = f'{path}/{parametres[4]["name"]}'

def get_warehouse_balance():
    """
    Reads the current balance from the restaurant CSV file and prints it in a tabulated format.
    """
    from crud import read_csv
    warehouse = read_csv(warehouse_path)
    return False, print(tabulate(warehouse, headers='keys'))

# def create_new_distributor():
#     """
#     Prompts the user to input details for creating a new distributor. Validates each input using the
#     respective validation functions and appends the new distributor's details to the distributors CSV file
#     if all inputs are valid.
#     """
#     from crud import append_csv, read_csv
    
#     while True:
#         inputs = {}
#         input_texts = ['Enter company id: ', 'Enter company name: ', 'Enter company address: ', 'Enter distributor name: ', 'Enter distributor phone number: ']
        
#         for inp in input_texts:
#             # Prompt the user for input
#             txt = input(inp)
            
#             # Validate the input
#             validated_data = validate_distributor_inputs(txt, input_texts, inp)
#             if validated_data[0]:
#                 # Store the valid input in the inputs dictionary
#                 inputs[parametres[5]['headers'][input_texts.index(inp)]] = validated_data[1]
#             else:
#                 # If validation fails, break out of the loop
#                 break
        
#         # Check if all inputs are valid
#         if len(inputs.keys()) == len(input_texts):
#             # Append the new distributor's details to the CSV file
#             append_csv(distributor_path, [inputs])
#             return False, print('Distributor added successfully!')

def add_product():
    """
    Consolidates products from the invoice, merges quantities of identical products,
    and updates the warehouse with the consolidated products.
    """
    from crud import read_csv, update_csv
    from warehouse_validators import validate_product_by_date_company_product_one_item_price
    from utils import choices
    invoice = read_csv(invoice_path)
    warehouse = read_csv(warehouse_path)
    print(tabulate(invoice, headers='keys'))
    # Use a defaultdict to accumulate quantities of products by name and price
    products_by_name_and_price = defaultdict(lambda: {'measure unit': '', 'quantity': 0, 'id': None})
    consolidated_products = []
    for data in warehouse:
        consolidated_products.append(data)
    current_id = itertools.count(start=0)

    for data in invoice:
        product_key = (data['product'], float(data['one item price']))
        # If the product is not already in the dictionary, assign a new ID
        if product_key not in products_by_name_and_price:
            products_by_name_and_price[product_key] = {
                'measure unit': data['measure unit'],
                'quantity': float(data['quantity'])
            }
        else:
            # If the product is already in the dictionary, update its information
            products_by_name_and_price[product_key]['measure unit'] = data['measure unit']
            products_by_name_and_price[product_key]['quantity'] += float(data['quantity'])
    
    # Create a list of consolidated products
    while True:
        for (name, price), info in products_by_name_and_price.items():
            valid, data = validate_product_by_date_company_product_one_item_price(warehouse_path, invoice_path)
            if valid:
                product_data = {
                    'id': next(current_id),
                    'product': data['product'],
                    'measure unit': info['measure unit'],
                    'quantity': data['quantity'],
                    'one item price': float(data['one item price'])
                }
                for i in consolidated_products:
                    if not i == product_data:
                        consolidated_products.append(product_data)
                        break
                if len(consolidated_products) == 0:
                    consolidated_products.append(product_data)

                update_csv(warehouse_path, consolidated_products)
                choice = choices('Do you want to add another one? (Enter y or n) \n')
                if choice:
                    print(tabulate(invoice, headers='keys'))
                    continue
                else:
                    return False, None
            else:
                return False, None
            
        # Update the warehouse CSV with the consolidated products

def drop_product():
    from warehouse_validators import validate_product_by_id
    from crud import read_csv, update_csv
    from tabulate import tabulate

    """
    Allows the user to delete a product from the warehouse by its ID.
    Prevents deletion if it is the only product in the warehouse.
    Reassigns IDs after deletion to avoid gaps.
    """
    while True:
        # Read current warehouse data
        warehouse_data = read_csv(warehouse_path)
        print(tabulate(warehouse_data, headers='keys'))
        
        # Prompt user for product ID or exit command
        product_id = input('Enter product id to delete or type "exit" to exit: ')

        if product_id == 'exit':
            return False, None
        
        # Validate if the product exists
        check_product = validate_product_by_id(product_id)
        if check_product:
            # Prevent deletion if it's the only product in the warehouse
            if len(warehouse_data) == 1 and warehouse_data[0]['id'] == product_id:
                print("Cannot remove the only element in the warehouse.")
                return False, None
            
            
            
            # Create a new list excluding the product to be deleted
            new_data = [data for data in warehouse_data if data['id'] != product_id]
            
            # Reassign IDs to avoid gaps
            for index, data in enumerate(new_data):
                data['id'] = str(index)  # Convert to string if IDs are strings

            # Update the CSV file with the new data
            update_csv(warehouse_path, new_data)
            print('Product deleted and IDs reassigned.')
            return True, None
        else:
            print('This product id doesn\'t exist!')
            continue

        

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

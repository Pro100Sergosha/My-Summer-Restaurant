from crud import read_csv, update_csv
from collections import defaultdict
from params import params
from tabulate import tabulate

restourant_path = f'files/{params[4]['name']}'
warehouse_path = f'files/{params[2]['name']}'
invoice_path = f'files/{params[1]['name']}'

def get_warehouse_balance():
    warehouse = read_csv(restourant_path)
    balance = warehouse[0]['budget']
    balance = [[balance]]
    return print(tabulate(balance, headers=['balance']))

def add_products():
    invoice = read_csv(invoice_path)
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

    for (name, price), info in products_by_name_and_price.items():
        product_data = {
            'id': info['id'],
            'product': name,
            'measure unit': info['measure unit'],
            'quantity': info['quantity'],
            'one item price': price
        }
        consolidated_products.append(product_data)

    update_csv(warehouse_path, consolidated_products)

def drop_product():
    while True:
        warehouse_data = read_csv(warehouse_path)
        print(tabulate(warehouse_data, headers='keys'))
        product_id = input('Enter product id to delete or exit to exit: ')
        new_data = []
        if len(warehouse_data) == 1 and warehouse_data[0]['id'] == product_id:
            return print("Cannot remove the only element in the warehouse_data.")
        elif product_id == 'exit':
            return print('Goodbye!')
        else:
            for data in warehouse_data:
                if data['id'] != product_id:
                    new_data.append(data)
        update_csv(warehouse_path, new_data)


def extract_product(product, amount, one_item_price):
    warehouse = read_csv(warehouse_path)
    new_data = []
    for data in warehouse:
        if data['product'] == product and data['one item price'] == one_item_price:
            data['quantity'] = float(data['quantity']) - float(amount)
            new_data.append(data)
        else:
            new_data.append(data)
    update_csv(warehouse_path, new_data)

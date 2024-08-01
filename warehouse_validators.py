from crud import read_csv
from warehouse import warehouse_path, invoice_path
import re
import csv

def read_csv(file_path):
    with open(file_path, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        return list(reader)

def validate_product_by_id(product_id):
    instance = read_csv(warehouse_path)
    for data in instance:
        if data['id'] == product_id:
            return True
    return False

def validate_date():
    while True:
        invoice = read_csv(invoice_path)
        
        date = input('Enter date (DD-MM-YYYY): ')
        if re.match(r'\d{2}-\d{2}-\d{4}', date):
            for data in invoice:
                if data['date'] == date:
                    return True, date
            print('Invoice with this date not found')
        else:
            print(f'Invalid date format\nPlease enter date in this format DD-MM-YYYY')

def validate_company_name():
    while True:
        invoice = read_csv(invoice_path)
        company_name = input('Enter company name: ')
        for data in invoice:
            if data['company name'] == company_name:
                return True, company_name
        print('Invoice with this company name not found')

def validate_product_name():
    while True:
        invoice = read_csv(invoice_path)
        product_name = input('Enter product name: ')
        for data in invoice:
            if data['product'] == product_name:
                return True, product_name
        print('Invoice with this product not found')

def validate_one_item_price():
    while True:
        try:    
            invoice = read_csv(invoice_path)
            one_item_price = input('Enter one item price: ')
            one_item_price_float = float(one_item_price)
            for data in invoice:
                if float(data['one item price']) == one_item_price_float:
                    return True, one_item_price_float
            print('Invoice with this one item price not found')
        except ValueError:
            print('Invalid price! Please enter a numeric value.')

def validate_product_existence(product_name, one_item_price, warehouse_path):
    warehouse = read_csv(warehouse_path)
    for data in warehouse:
        if product_name == data['product'] and one_item_price == float(data['one item price']):
            return True
    return False

def validate_product_by_date_company_product_one_item_price(warehouse_path, invoice_path):
    while True:
        date_valid = validate_date()
        company_name_valid = validate_company_name()
        product_name_valid = validate_product_name()
        one_item_price_valid = validate_one_item_price()
        
        product_exists = validate_product_existence(product_name_valid[1], one_item_price_valid[1], warehouse_path)
        
        if not product_exists:
            invoice = read_csv(invoice_path)
            for data in invoice:
                if (data['date'] == date_valid[1] and 
                    data['company name'] == company_name_valid[1] and 
                    data['product'] == product_name_valid[1] and 
                    data['one item price'] == str(one_item_price_valid[1])):
                    return True, data
            print('No matching invoice found.')
        else:
            print('This product is already in the warehouse.')

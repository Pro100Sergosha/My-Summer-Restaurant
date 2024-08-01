from parametres import parametres
from creator import folder_path

from utils import choices

path = folder_path()

# Define paths for invoice and warehouse files
invoice_path = f'{path}/{parametres[4]["name"]}'
warehouse_path = f'{path}/{parametres[2]["name"]}'

def create_invoice_with_data(input_texts):
    from invoice_validators import data, validate_invoice_inputs
    from crud import update_csv, read_csv
    from collections import defaultdict
    """
    Creates an invoice using previously validated data and additional inputs from the user.
    Consolidates products with the same date, company, product name, and one item price.
    """
    inputs = {}
    parametres = ['date', 'company name', 'product', 'measure unit', 'quantity', 'one item price']

    # Use previously validated date and company name
    inputs['date'] = data[0][1]
    inputs['company name'] = data[1][1]

    # Collect and validate additional inputs
    for inp in input_texts[2:]:
        again_txt = input(inp)
        again_data = validate_invoice_inputs(again_txt, input_texts, inp)
        if again_data[0]:
            inputs[parametres[input_texts.index(inp)]] = again_data[1]
        else:
            print(f"Invalid input for {inp}")
            return False, None

    if len(inputs.keys()) == len(input_texts):
        # Calculate total price
        inputs['total price'] = float(inputs['quantity']) * float(inputs['one item price'])

        # Read existing invoices
        existing_invoices = read_csv(invoice_path)
        products_by_date_company = defaultdict(lambda: {'measure unit': '', 'quantity': 0, 'one item price': 0, 'total price': 0})

        # Consolidate products
        for invoice in existing_invoices:
            product_key = (invoice['date'], invoice['company name'], invoice['product'], float(invoice['one item price']))
            if product_key in products_by_date_company:
                products_by_date_company[product_key]['quantity'] += float(invoice['quantity'])
                products_by_date_company[product_key]['total price'] += float(invoice['total price'])
            else:
                products_by_date_company[product_key] = {
                    'measure unit': invoice['measure unit'],
                    'quantity': float(invoice['quantity']),
                    'one item price': float(invoice['one item price']),
                    'total price': float(invoice['total price'])
                }

        # Add new product
        new_product_key = (inputs['date'], inputs['company name'], inputs['product'], float(inputs['one item price']))
        if new_product_key in products_by_date_company:
            products_by_date_company[new_product_key]['quantity'] += float(inputs['quantity'])
            products_by_date_company[new_product_key]['total price'] += inputs['total price']
        else:
            products_by_date_company[new_product_key] = {
                'measure unit': inputs['measure unit'],
                'quantity': float(inputs['quantity']),
                'one item price': float(inputs['one item price']),
                'total price': inputs['total price']
            }

        # Prepare consolidated products for CSV update
        consolidated_invoices = []
        for (date, company_name, product, one_item_price), info in products_by_date_company.items():
            consolidated_invoices.append({
                'date': date,
                'company name': company_name,
                'product': product,
                'measure unit': info['measure unit'],
                'quantity': info['quantity'],
                'one item price': one_item_price,
                'total price': info['total price']
            })

        # Update the CSV file with consolidated invoices
        update_csv(invoice_path, consolidated_invoices)
        print(f'Invoice created successfully!\n')

        return True, None
    else:
        return False, None

def create_new_invoice():
    from crud import read_csv, update_csv
    from collections import defaultdict
    from invoice_validators import validate_invoice_inputs
    """
    Collects user inputs to create a new invoice and optionally creates additional invoices with the same date and company name.
    Consolidates products with the same date, company, product name, and one item price.
    """
    while True:
        inputs = {}
        input_texts = ['Enter date: ', 'Enter company name: ', 'Enter product name: ', 'Enter measure unit: ', 'Enter quantity: ', 'Enter one item price: ']
        parametres = ['date', 'company name', 'product', 'measure unit', 'quantity', 'one item price']

        # Collect and validate inputs for the new invoice
        for inp in input_texts:
            txt = input(inp)
            validated_data = validate_invoice_inputs(txt, input_texts, inp)
            if validated_data[0]:
                inputs[parametres[input_texts.index(inp)]] = validated_data[1]
            else:
                return False, None

        if len(inputs.keys()) == len(input_texts):
            # Calculate total price
            inputs['total price'] = float(inputs['quantity']) * float(inputs['one item price'])

            # Read existing invoices
            existing_invoices = read_csv(invoice_path)
            products_by_date_company = defaultdict(lambda: {'measure unit': '', 'quantity': 0, 'one item price': 0, 'total price': 0})

            # Consolidate products
            for invoice in existing_invoices:
                product_key = (invoice['date'], invoice['company name'], invoice['product'], float(invoice['one item price']))
                if product_key in products_by_date_company:
                    products_by_date_company[product_key]['quantity'] += float(invoice['quantity'])
                    products_by_date_company[product_key]['total price'] += float(invoice['total price'])
                else:
                    products_by_date_company[product_key] = {
                        'measure unit': invoice['measure unit'],
                        'quantity': float(invoice['quantity']),
                        'one item price': float(invoice['one item price']),
                        'total price': float(invoice['total price'])
                    }

            # Add new product
            new_product_key = (inputs['date'], inputs['company name'], inputs['product'], float(inputs['one item price']))
            if new_product_key in products_by_date_company:
                products_by_date_company[new_product_key]['quantity'] += float(inputs['quantity'])
                products_by_date_company[new_product_key]['total price'] += inputs['total price']
            else:
                products_by_date_company[new_product_key] = {
                    'measure unit': inputs['measure unit'],
                    'quantity': float(inputs['quantity']),
                    'one item price': float(inputs['one item price']),
                    'total price': inputs['total price']
                }

            # Prepare consolidated products for CSV update
            consolidated_invoices = []
            for (date, company_name, product, one_item_price), info in products_by_date_company.items():
                consolidated_invoices.append({
                    'date': date,
                    'company name': company_name,
                    'product': product,
                    'measure unit': info['measure unit'],
                    'quantity': info['quantity'],
                    'one item price': one_item_price,
                    'total price': info['total price']
                })

            # Update the CSV file with consolidated invoices
            update_csv(invoice_path, consolidated_invoices)
            print(f'Invoice created successfully!\n')

            # Ask the user if they want to create another invoice with the same date and company
            while True:
                again = choices('Do you want to create a new invoice with this date and company? (Enter y or n) \n')
                if again:
                    create_invoice_with_data(input_texts)
                else:
                    from debts import add_debt
                    add_debt()
                    print('Goodbye!')
                    return False, None
        else:
            return False, None


if __name__ == '__main__':
    create_new_invoice()
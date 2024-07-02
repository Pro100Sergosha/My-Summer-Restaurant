from parametres import parametres
from creator import folder_path

from warehouse import add_products

from utils import choices

path = folder_path()

invoice_path = f'{path}/{parametres[4]["name"]}'
warehouse_path = f'{path}/{parametres[2]["name"]}'


def create_invoice_with_data(input_texts):
    from invoice_validators import data, validate_invoice_inputs
    from crud import append_csv
    inputs = {}
    inputs[parametres[4]['headers'][0]] = data[0][1]
    inputs[parametres[4]['headers'][1]] = data[1][1]
    for inp in input_texts[2:]:
        again_txt = input(inp)
        again_data = validate_invoice_inputs(again_txt, input_texts, inp)
        if again_data[0]:
            inputs[parametres[4]['headers'][input_texts.index(inp)]] = again_data[1]
        else:
            break
        if len(inputs.keys()) == len(input_texts):
            inputs[parametres[4]['headers'][6]] = float(inputs['quantity']) * float(inputs['one item price'])
            add_products()
            append_csv(invoice_path, [inputs])
            return print(f'Invoice created successfuly!\n')


def create_new_invoice():
    from crud import append_csv
    from invoice_validators import validate_invoice_inputs
    while True:
        inputs = {}
        input_texts = ['Enter date: ', 'Enter company name: ', 'Enter product name: ', 'Enter measure unit: ', 'Enter quantity: ', 'Enter one item price: ']
        for inp in input_texts:
            txt = input(inp)
            validated_data = validate_invoice_inputs(txt, input_texts, inp)
            if validated_data[0]:
                inputs[parametres[4]['headers'][input_texts.index(inp)]] = validated_data[1]
            elif not validated_data[0]:
                return False, None
        if len(inputs.keys()) == len(input_texts):
            inputs[parametres[4]['headers'][6]] = float(inputs['quantity']) * float(inputs['one item price'])
            append_csv(invoice_path, [inputs])
            print(f'Invoice created successfuly!\n')
            while True:
                again = choices('Do you want to create new invoice with this date and company?(Enter y or n) \n')
                if again:
                    create_invoice_with_data(input_texts)
                else:
                    from debts import add_debt
                    add_debt()
                    add_products()
                    return False, print('Goodbye!')
        
        
            

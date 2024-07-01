from params import params
from crud import append_csv, read_csv, update_csv
from warehouse import add_products
from invoice_validators import data, validate_invoice_inputs
from utils import choices

invoice_path = f'files/{params[1]['name']}'
warehouse_path = f'files/{params[2]['name']}'


def create_invoice_with_data(input_texts):
    inputs = {}
    inputs[params[1]['headers'][0]] = data[0][1]
    inputs[params[1]['headers'][1]] = data[1][1]
    for inp in input_texts[2:]:
        again_txt = input(inp)
        again_data = validate_invoice_inputs(again_txt, input_texts, inp)
        if again_data[0]:
            inputs[params[1]['headers'][input_texts.index(inp)]] = again_data[1]
        else:
            break
        if len(inputs.keys()) == len(input_texts):
            inputs[params[1]['headers'][6]] = float(inputs['quantity']) * float(inputs['one item price'])
            add_products()
            append_csv(invoice_path, [inputs])
            return print(f'Invoice created successfuly!\n')


def create_new_invoice(input_texts):
    while True:
        inputs = {}
        input_texts = ['Enter date: ', 'Enter company name: ', 'Enter product name: ', 'Enter measure unit: ', 'Enter quantity: ', 'Enter one item price: ']
        for inp in input_texts:
            txt = input(inp)
            validated_data = validate_invoice_inputs(txt, input_texts, inp)
            if validated_data[0]:
                inputs[params[1]['headers'][input_texts.index(inp)]] = validated_data[1]
            else:
                break
        if len(inputs.keys()) == len(input_texts):
            inputs[params[1]['headers'][6]] = float(inputs['quantity']) * float(inputs['one item price'])
            append_csv(invoice_path, [inputs])
            print(f'Invoice created successfuly!\n')
            while True:
                again = choices('Do you want to create new invoice with this date and company? \n')
                if again:
                    create_invoice_with_data(input_texts)
                else:
                    from debts import add_debt
                    add_debt()
                    add_products()
                    return print('Goodbye!')
        
        
            

if __name__ == '__main__':
    create_new_invoice()
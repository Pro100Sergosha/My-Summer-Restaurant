import re
from distributor_validators import check_distributor_existence

def validate_date(text, input_texts, inp):
    while True:
        if input_texts.index(inp) == 0 and re.match(r'\d{2}-\d{2}-\d{4}', text):
            return True, text
        elif input_texts.index(inp) == 0 and not re.match(r'\d{2}-\d{2}-\d{4}', text):
            print(f'Invalid date format\nPlease enter date in this format DD-MM-YYYY')
            text = input(inp)
        else:
            return False, 'txt'

def validate_distributor(text, input_texts, inp):
    while True:
        if input_texts.index(inp) == 1 and check_distributor_existence(text):
            return True, text
        elif input_texts.index(inp) == 1 and not check_distributor_existence(text):
            print(f'Company with this name doesn\'t exist')
            text = input(inp)
        else:
            return False, 'txt'

def validate_measure_unit(text, input_texts, inp):
    while True:
        if input_texts.index(inp) == 3 and not text in ['piece', 'kg', 'litres']:
            print(f'Invalid measure unit\nPlease enter one from this - (piece, kg, litres)')
            text = input(inp)
        if input_texts.index(inp) == 3 and  text in ['piece', 'kg', 'litres']:
            return True, text
        else:
            return False, 'txt'

def validate_quantity(text, measure_unit, input_texts, inp):
    while True:
        try:
            if input_texts.index(inp) == 4 and not measure_unit[1] in ['kg', 'litres']:
                return True, float(text)
            elif input_texts.index(inp) == 4 and measure_unit[1] != 'piece':
                return True, int(text)
            else:
                return False, 'txt'
        except ValueError:
            print(f'Invalid number\nPlease enter integer value')
            text = input(inp)



def validate_product_name(text, input_texts, inp):
    while True:
        if input_texts.index(inp) == 2 and text.strip() == '':
            print(f'Product name must be filled in!')
            text = input(inp)
        if input_texts.index(inp) == 2 and text:
            return True, text.title()
        else:
            return False, 'txt'
        
def validate_one_item_input(text, input_texts, inp):
    while True:
        try:
            if input_texts.index(inp) == 5 and text.strip() == '':
                raise ValueError
            else:
                return True, float(text)
        except ValueError:
            print('Wrong type!\nPlease enter numbers')
            text = input(inp)
data = []
def validate_invoice_inputs(text, input_texts, inp):
    date = validate_date(text, input_texts, inp)
    if date[0]:
        data.append(date)
        return date
    
    distributor = validate_distributor(text, input_texts, inp)
    if distributor[0]:
        data.append(distributor)
        return distributor
    
    product_name = validate_product_name(text, input_texts, inp)
    if product_name[0]:
        return product_name
    measure_unit = validate_measure_unit(text, input_texts, inp)
    if measure_unit[0]:
        data.append(measure_unit)
        return measure_unit
    quantity = validate_quantity(text, data[2], input_texts, inp)
    if quantity[0]:
        return quantity
    one_item_price = validate_one_item_input(text, input_texts, inp)
    if one_item_price[0]:
        return one_item_price
    
import re

def is_float(s):
    """
    Checks if the given string can be converted to a float.
    """
    try:
        float(s)
        return True
    except ValueError:
        return False

def validate_date(text, input_texts, inp):
    """
    Validates that the input text is a date in the format DD-MM-YYYY.
    """
    while True:
        if input_texts.index(inp) == 0 and re.match(r'\d{2}-\d{2}-\d{4}', text):
            return True, text
        elif input_texts.index(inp) == 0 and not re.match(r'\d{2}-\d{2}-\d{4}', text):
            print(f'Invalid date format\nPlease enter date in this format DD-MM-YYYY')
            text = input(inp)
        else:
            return False, 'date'

def validate_distributor(text, input_texts, inp):
    """
    Validates that the distributor exists in the system.
    """
    from distributor_validators import check_distributor_existence
    while True:
        if check_distributor_existence(text) and input_texts.index(inp) == 1:
            return True, text
        elif not check_distributor_existence(text) and input_texts.index(inp) == 1:
            print(f'Company with this name doesn\'t exist \nEnter existing company name or type exit to exit')
            while True:
                text = input(inp)
                if check_distributor_existence(text):
                    return True, text
                else:
                    if text == 'exit':
                        return False, 'create'
                    else:
                        print('Invalid input')
        else:
            return False, 'continue iteration'

def validate_measure_unit(text, input_texts, inp):
    """
    Validates that the measure unit is one of the accepted values: 'piece', 'kg', 'litres'.
    """
    while True:
        if input_texts.index(inp) == 3 and not text in ['piece', 'kg', 'litres']:
            print(f'Invalid measure unit\nPlease enter one from this - (piece, kg, litres)')
            text = input(inp)
        if input_texts.index(inp) == 3 and text in ['piece', 'kg', 'litres']:
            return True, text
        else:
            return False, 'measure unit'

def validate_quantity(text, measure_unit, input_texts, inp):
    """
    Validates the quantity based on the measure unit. Ensures the quantity is a float for 'kg' and 'litres' and an integer for 'piece'.
    """
    while True:
        try:
            if input_texts.index(inp) == 4 and measure_unit[1] in ['kg', 'litres']:
                return True, float(text)
            elif input_texts.index(inp) == 4 and measure_unit[1] == 'piece':
                text = int(text)
                return True, text
            elif is_float(text):
                return False, 'quantity'
            elif not is_float(text):
                raise ValueError
        except ValueError:
            print(f'Invalid number\nPlease enter integer value')
            text = input(inp)

def validate_product_name(text, input_texts, inp):
    """
    Validates that the product name is not empty.
    """
    while True:
        if input_texts.index(inp) == 2 and text.strip() == '':
            print(f'Product name must be filled in!')
            text = input(inp)
        if input_texts.index(inp) == 2 and text:
            return True, text.title()
        else:
            return False, 'product name'
        
def validate_one_item_input(text, input_texts, inp):
    """
    Validates that the input text is a float, which represents the price of one item.
    """
    while True:
        try:
            if input_texts.index(inp) == 5 and text.strip() == '':
                raise ValueError
            elif not is_float(text):
                return False, 'Not Float'
            else:
                return True, float(text)
        except ValueError:
            print('Wrong type!\nPlease enter numbers')
            text = input(inp)

# List to store validated data
data = []

def validate_invoice_inputs(text, input_texts, inp):
    """
    Validates various invoice inputs such as date, distributor, product name, measure unit, quantity, and one item price.
    """
    try:
        date = validate_date(text, input_texts, inp)
        if date[0] and not date in data:
            data.append(date)
            return date

        distributor = validate_distributor(text, input_texts, inp)
        if distributor[0] and not distributor in data:
            data.append(distributor)
            return distributor
        elif distributor[1] == 'create' and not distributor[0]:
            return False, print('Please create new distributor and try again')
        product_name = validate_product_name(text, input_texts, inp)
        if product_name[0] and not product_name in data:
            data.append(product_name)
            return product_name
        
        measure_unit = validate_measure_unit(text, input_texts, inp)
        if measure_unit[0] and not measure_unit in data:
            data.append(measure_unit)
            return measure_unit
        
        quantity = validate_quantity(text, data[3], input_texts, inp)
        if quantity[0] and not quantity in data:
            data.append(quantity)
            return quantity
        
        one_item_price = validate_one_item_input(text, input_texts, inp)
        if one_item_price[0] and not one_item_price in data:
            data.append(one_item_price)
            del data[2:]
            return one_item_price
    except IndexError:
        return False, None
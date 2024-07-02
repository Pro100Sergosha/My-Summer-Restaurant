from parametres import parametres
from creator import folder_path
import re

path = folder_path()

distributor_path = f'{path}/{parametres[5]["name"]}'

def validate_company_id(text, input_texts, inp):
    from crud import read_csv
    while True:
        try:
            if input_texts.index(inp) == 0 and re.match(r'^\d{9}$|^\d{11}$', text):
                company_id = [company_id for company_id in read_csv(distributor_path) if text == company_id['id']]
                if company_id:
                    raise Exception
                return True, int(text)
            elif input_texts.index(inp) != 0:
                return False, 'txt'
            else:
                raise ValueError
        except ValueError:
            print('Invalid type!\nPlease enter integer numbers which length is 9 or 11')
            text = input(inp)
        except Exception:
            print('Company with this id already exists.')
            text = input(inp)

def validate_company_name(text, input_texts, inp):
    while True:
        try:
            if input_texts.index(inp) == 1 and re.match(r'^[A-Za-z\s]+$', text):
                return True, text
            elif input_texts.index(inp) != 1:
                return False, 'txt'
            else:
                raise ValueError("Invalid company name format.")
        except ValueError:
            print('Invalid type!\nPlease enter a valid company name (letters and spaces only).')
            text = input(inp)

def validate_company_address(text, input_texts, inp):
    while True:
        try:
            if input_texts.index(inp) == 2 and text.strip() != '':
                return True, text
            elif input_texts.index(inp) != 2:
                return False, 'txt'
            else:
                raise ValueError("Invalid company address.")
        except ValueError:
            print('Invalid type!\nPlease enter a valid company address.')
            text = input(inp)

def validate_distributor_name(text, input_texts, inp):
    while True:
        try:
            if input_texts.index(inp) == 3 and re.match(r'^[A-Za-z\s]+$', text):
                return True, text
            elif input_texts.index(inp) != 3:
                return False, 'txt'
            else:
                raise ValueError("Invalid distributor name format.")
        except ValueError:
            print('Invalid type!\nPlease enter a valid distributor name (letters and spaces only).')
            text = input(inp)

def validate_distributor_phone_number(text, input_texts, inp):
    while True:
        try:
            if input_texts.index(inp) == 4 and re.match(r'\d{3}[- ]\d{2}[- ]\d{2}[- ]\d{2}', text):
                return True, text
            elif input_texts.index(inp) != 4:
                return False, 'txt'
            else:
                raise ValueError("Invalid phone number format.")
        except ValueError:
            print('Invalid type!\nPlease enter a valid phone number ( 123-45-67-89 or 123 45 67 89).')
            text = input(inp)

def check_distributor_existence(distrib):
    from crud import read_csv
    instance = read_csv(distributor_path)
    for data in instance:
        if data['company name'] == distrib:
            return True
    return False

def validate_distributor_inputs(text, input_texts, inp):
    company_id = validate_company_id(text, input_texts, inp)
    if company_id[0]:
        return company_id
    company_name = validate_company_name(text, input_texts, inp)
    if company_name[0]:
        return company_name
    company_address = validate_company_address(text, input_texts, inp)
    if company_address[0]:
        return company_address
    distributor_name = validate_distributor_name(text, input_texts, inp)
    if distributor_name[0]:
        return distributor_name
    phone_number = validate_distributor_phone_number(text, input_texts, inp)
    if phone_number[0]:
        return phone_number
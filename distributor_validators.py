from parametres import parametres
from creator import folder_path
import re

path = folder_path()

# Path to the distributors CSV file
distributor_path = f'{path}/{parametres[5]["name"]}'

def validate_company_id(text, input_texts, inp):
    """
    Validates the company ID to ensure it is either 9 or 11 digits long and is unique.
    Returns True and the ID if valid, otherwise prompts the user to re-enter the ID.
    """
    from crud import read_csv
    while True:
        try:
            if input_texts.index(inp) == 0 and re.match(r'^\d{9}$|^\d{11}$', text):
                # Check if the company ID already exists
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
    """
    Validates the company name to ensure it only contains letters and spaces.
    Returns True and the name if valid, otherwise prompts the user to re-enter the name.
    """
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
    """
    Validates the company address to ensure it is not empty.
    Returns True and the address if valid, otherwise prompts the user to re-enter the address.
    """
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
    """
    Validates the distributor name to ensure it only contains letters and spaces.
    Returns True and the name if valid, otherwise prompts the user to re-enter the name.
    """
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
    """
    Validates the distributor's phone number to ensure it follows the format 123-45-67-89 or 123 45 67 89.
    Returns True and the phone number if valid, otherwise prompts the user to re-enter the phone number.
    """
    while True:
        try:
            if input_texts.index(inp) == 4 and re.match(r'\d{3}[- ]\d{2}[- ]\d{2}[- ]\d{2}', text):
                return True, text
            elif input_texts.index(inp) != 4:
                return False, 'txt'
            else:
                raise ValueError("Invalid phone number format.")
        except ValueError:
            print('Invalid type!\nPlease enter a valid phone number (123-45-67-89 or 123 45 67 89).')
            text = input(inp)

def check_distributor_existence(distrib):
    """
    Checks if a distributor with the given company name already exists in the CSV file.
    Returns True if the distributor exists, otherwise returns False.
    """
    from crud import read_csv
    instance = read_csv(distributor_path)
    for data in instance:
        if data['company name'] == distrib:
            return True
    return False

def validate_distributor_inputs(text, input_texts, inp):
    """
    Validates various distributor inputs (company ID, name, address, distributor name, and phone number)
    by calling respective validation functions.
    """
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

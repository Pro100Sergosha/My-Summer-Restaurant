import csv
from creator import folder_path

path = folder_path()

file_path = f'{path}/'

def check_create_headers(filename, data):
    headers = list(data[0].keys())
    with open(filename, 'r+', newline='') as f:
        reader = csv.DictReader(f)
        writer = csv.DictWriter(f, fieldnames=headers)
        if reader.fieldnames == None:
            writer.writeheader()
            return False
        else:
            return True

def choices(txt):
    while True:
        again = input(txt)
        if again == 'y':
            return True
        elif again == 'n':
            return False
        else:
            print('Wrong choice! Enter y or n')
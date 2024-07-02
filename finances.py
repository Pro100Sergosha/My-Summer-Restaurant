from tabulate import tabulate
from parametres import parametres
from creator import folder_path

path = folder_path()

# Paths to debts and restaurant CSV files
debts_path = f'{path}/{parametres[6]["name"]}'
restourant_path = f'{path}/{parametres[-1]["name"]}'

def get_warehouse_balance():
    """
    Reads the current balance from the restaurant CSV file and prints it in a tabulated format.
    """
    from crud import read_csv
    warehouse = read_csv(restourant_path)
    balance = warehouse[0]['budget']
    balance = [[balance]]
    return False, print(tabulate(balance, headers=['balance']))

def get_financial_report(option):
    """
    Generates and prints a financial report of unpaid debts, displaying their status (Unpaid, In Progress, Paid).
    Filters the report based on the user's input option.
    """
    from crud import read_csv
    debts = read_csv(debts_path)
    unpaid_list = []
    
    for data in debts:
        report = {}
        unpaid = data['unpaid']
        paid = data['paid']
        date = data['date']
        balance = read_csv(restourant_path)[0]['budget']
        unpaid_amount = float(unpaid)
        paid_amount = float(paid)
        
        if paid_amount == 0:
            status = 'Unpaid'
        elif paid_amount < unpaid_amount:
            status = 'In Progress'
        else:
            status = 'Paid'
        
        report['date'] = date
        report['unpaid'] = unpaid
        report['paid'] = paid
        report['status'] = status
        report['balance'] = balance
        unpaid_list.append(report)
    
    filtered_list = []
    opt = input(option)
    
    for unpaid in unpaid_list:
        if opt in ['paid', 'unpaid', 'in progress'] and str(unpaid.get('status', '')).lower() == str(opt).lower():
            filtered_list.append(unpaid)
        if opt == '':
            filtered_list.append(unpaid)
    
    print(tabulate(filtered_list, tablefmt='fancy_grid', headers='keys'))

def date_to_int(date_str):
    """
    Converts a date string in the format 'DD-MM-YYYY' to an integer in the format YYYYMMDD for easy comparison.
    """
    day, month, year = map(int, date_str.split('-'))
    return year * 10000 + month * 100 + day

def get_report_with_date():
    """
    Generates and prints a financial report of total unpaid and paid amounts within a specified date range.
    Prompts the user to enter the start and end dates for the report.
    """
    from crud import read_csv
    debts = read_csv(debts_path)
    balance = float(read_csv(restourant_path)[0]['budget'])

    total_unpaid = 0
    total_paid = 0
    start_date = input('Enter start date: ')
    end_date = input('Enter end date: ')
    start_date_int = date_to_int(start_date)
    end_date_int = date_to_int(end_date)

    for data in debts:
        unpaid = data['unpaid']
        paid = data['paid']
        date = data['date']
        
        date_int = date_to_int(date)
    
        if start_date_int <= date_int <= end_date_int:
            unpaid_amount = float(unpaid)
            paid_amount = float(paid)
            
            total_unpaid += unpaid_amount
            total_paid += paid_amount

    overall_info = {
        'start_date': start_date,
        'end_date': end_date,
        'total_unpaid': total_unpaid,
        'total_paid': total_paid,
        'total_balance': balance,
        'income': 0
    }

    return False, print(tabulate([overall_info], headers='keys'))

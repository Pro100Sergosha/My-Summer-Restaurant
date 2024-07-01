from crud import read_csv
from tabulate import tabulate
from params import params
import datetime

debts_path = f'files/{params[3]['name']}'
restourant_path = f'files/{params[4]['name']}'

def get_financial_report(option):
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

        if opt  in ['paid', 'unpaid', 'in progress'] and str(unpaid.get('status', '')).lower() == str(opt).lower():
            filtered_list.append(unpaid)
        if opt == '':
            filtered_list.append(unpaid)
    print(tabulate(filtered_list, tablefmt='fancy_grid', headers='keys'))
    
def get_report_with_date(start_date, end_date):
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
        
        # Filter by date range (assuming dates are in the format 'YYYY-MM-DD')
        if start_date <= date <= end_date:
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

    print(tabulate(unpaid_list, tablefmt='fancy_grid', headers='keys'))
    
    total_unpaid = sum(float(report['unpaid']) for report in unpaid_list)
    total_paid = sum(float(report['paid']) for report in unpaid_list)
    total_balance = read_csv(restourant_path)[0]['budget']

    overall_info = {
        'total_unpaid': total_unpaid,
        'total_paid': total_paid,
        'total_balance': total_balance
    }

    return overall_info


get_report_with_date('01-07-2023','31-07-2023')
# get_financial_report('Enter which status do you want (paid, unpaid, in progress) or nothing to see all: ')
    
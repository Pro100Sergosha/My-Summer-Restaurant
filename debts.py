from crud import read_csv, append_csv, write_csv, update_csv
from invoices import invoice_path
from params import params
from collections import defaultdict
from tabulate import tabulate

debts_path = f'files/{params[3]['name']}'
balance_path = f'files/{params[4]['name']}'
warehouse_path = f'files/{params[2]['name']}'

def check_old_debts(new_debts, old_debts):
    updated_data = []
    for new in new_debts:
        for old in old_debts:
            if new['date'] == old['date'] and new['company name'] == old['company name']:
                new['paid'] = old['paid']
                break
        updated_data.append(new)
    return updated_data


def add_debt():
    invoice = read_csv(invoice_path)
    old_debt_list = read_csv(debts_path)
    debts_by_date_and_distributor = defaultdict(float)
    new_debt_list = []
    for data in invoice:
        debts_data = {key: data[key] for key in ['date', 'company name', 'total price']}
        debts_data['unpaid'] = debts_data['total price']
        debts_by_date_and_distributor[(data['date'], data['company name'])] += float(debts_data['unpaid'])

    for (date, distributor), unpaid_amount in debts_by_date_and_distributor.items():
        debts_data = {}
        debts_data['date'] = date
        debts_data['company name'] = distributor
        debts_data['unpaid'] = unpaid_amount
        debts_data['paid'] = 0
        new_debt_list.append(debts_data)
    data = check_old_debts(new_debt_list, old_debt_list)
    update_csv(debts_path, data)

def check_debt_amount(debts, debt, unpaid, paid):
    budget = read_csv(balance_path)
    balance = float(budget[0]['budget'])
    while True:
        try:
            amount = float(input('Enter amount of money you want to pay: '))
            if balance >= amount:
                if unpaid >= paid and paid + amount <= unpaid:
                    budget[0]['budget'] = balance - amount
                    debt['paid'] = float(debt['paid']) + amount
                    write_csv(balance_path, budget)
                    return debts
                else:
                    print('Too much money')
            else:
                print('Not enough money')
        except ValueError:
            print('Invalid type!\nPlease enter only int or float numbers!')


def pay_debt():
    while True:
        debts = read_csv(debts_path)
        balance = read_csv(balance_path)[0]['budget']
        temp_list = []
        for data in debts:
            temp_debt = {key: data[key] for key in ['date', 'company name', 'unpaid', 'paid']}
            temp_list.append(temp_debt)
        print(tabulate(temp_list, headers='keys'))
        date = input('Enter date: ')
        distributor = input('Enter company name: ')
        for debt in debts:
            if debt['date'] == date and debt['company name'] == distributor:
                date = debt['date']
                distributor = debt['company name']
                unpaid = float(debt['unpaid'])
                paid = float(debt['paid'])
                debt['balance'] = balance
                table = [date, distributor, unpaid, paid]   
                print(tabulate([table], tablefmt='grid', headers=debt.keys()))
                new_debts = check_debt_amount(debts, debt, unpaid, paid)
                update_csv(debts_path, new_debts)
                return True
                

def pay_salaries():
    balance = read_csv(balance_path)
    if float(balance[0]['budget']) - float(balance[0]['salary']) >= 0:
        balance[0]['budget'] = float(balance[0]['budget']) - float(balance[0]['salary'])
        update_csv(balance_path, balance)
        return print('Salaries payed successfully')
    else:
        return print('Not enough money')
    

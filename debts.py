from invoices import invoice_path
from creator import folder_path
from parametres import parametres
from collections import defaultdict
from tabulate import tabulate

path = folder_path()

# Paths for various CSV files
debts_path = f'{path}/{parametres[6]["name"]}'
balance_path = f'{path}/{parametres[-1]["name"]}'
warehouse_path = f'{path}/{parametres[1]["name"]}'

def check_old_debts(new_debts, old_debts):
    """
    Checks if the new debts are already present in the old debts. If found, it updates the 'paid' amount
    from the old debts to the new debts.
    """
    updated_data = []
    for new in new_debts:
        for old in old_debts:
            if new['date'] == old['date'] and new['company name'] == old['company name']:
                new['paid'] = old['paid']
                break
        updated_data.append(new)
    return updated_data


def add_debt():
    """
    Reads the invoices and calculates the total unpaid amount for each company by date. It then updates the
    debts CSV file with this new data, maintaining any 'paid' amounts from the old debts.
    """
    from crud import read_csv, append_csv, write_csv, update_csv
    
    # Reading the current invoices and old debts
    invoice = read_csv(invoice_path)
    old_debt_list = read_csv(debts_path)
    
    # Calculating new debts
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
    
    # Updating the new debts with any old 'paid' amounts
    data = check_old_debts(new_debt_list, old_debt_list)
    update_csv(debts_path, data)

def check_debt_amount(debts, debt, unpaid, paid):
    """
    Prompts the user to enter an amount to pay towards a debt and updates the balance and debt records
    accordingly if the payment is valid.
    """
    from crud import read_csv, write_csv
    
    # Reading the current budget
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
                return False
        except ValueError:
            print('Invalid type!\nPlease enter only int or float numbers!')


def pay_debt():
    """
    Allows the user to pay a debt by specifying the date and company name. It validates the payment amount
    and updates the debts and balance CSV files accordingly.
    """
    from crud import read_csv, update_csv
    
    while True:
        # Reading the current debts and balance
        debts = read_csv(debts_path)
        balance = read_csv(balance_path)[0]['budget']
        
        # Displaying current debts
        temp_list = []
        for data in debts:
            temp_debt = {key: data[key] for key in ['date', 'company name', 'unpaid', 'paid']}
            temp_list.append(temp_debt)
        print(tabulate(temp_list, headers='keys'))
        
        # Getting user input for date and company name
        date = input('Enter date: ')
        company_name = input('Enter company name: ')
        
        for debt in debts:
            if debt['date'] == date and debt['company name'] == company_name:
                # Displaying selected debt details
                date = debt['date']
                company_name = debt['company name']
                unpaid = float(debt['unpaid'])
                paid = float(debt['paid'])
                table = {}
                table['date'] = date
                table['company name'] = company_name
                table['unpaid'] = unpaid
                table['paid'] = paid
                table['balance'] = balance
                print(tabulate([table], tablefmt='grid', headers='keys'))
                
                # Checking the debt amount to pay
                new_debts = check_debt_amount(debts, debt, unpaid, paid)
                if not new_debts:
                    return False, print('Bankrupt! :(')
                update_csv(debts_path, new_debts)
                return False, print('Paid successfully!')
        else:
            return False, print('This date or company doesn\'t exist')

def pay_salaries():
    """
    Pays the salaries from the current budget if there are sufficient funds. Updates the budget in the
    balance CSV file accordingly.
    """
    from crud import read_csv, update_csv
    
    # Reading the current balance
    balance = read_csv(balance_path)
    
    # Checking if there is enough money to pay the salaries
    if float(balance[0]['budget']) - float(balance[0]['salary']) >= 0:
        balance[0]['budget'] = float(balance[0]['budget']) - float(balance[0]['salary'])
        update_csv(balance_path, balance)
        return False, print('Salaries paid successfully')
    else:
        return False, print('Not enough money')

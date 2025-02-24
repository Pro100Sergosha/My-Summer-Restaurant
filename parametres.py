
departments = {
    'admin': [
        {
        'initiate restorant': [
                            'create/check necessary files',
                            'change tables number',
                            'change salary percent',
                            'change margin percent',
                            'change comission percent',
                            'change budget',
                            'back'
                            ],
        'user management': [
                        'add new user',
                        'edit user',
                        'delete user',
                        'back'
                        ], 
        'accountant management': [
                                'get financial report',
                                'get warehouse balance',
                                'calculate dish cost',
                                'add new distributor',
                                'pay debt',
                                'pay salaries',
                                'back'
                                ], 
        'warehouse management': [
                                'get warehouse balance',
                                'create new invoice',
                                'add new product',
                                'drop product',
                                'back'
                                ],
        'kitchen management': [
                                'add new dish', 
                                'edit dish',
                                'delete dish',
                                'get orders',
                                'give orders',
                                'back'
                                ], 
        'waiters management': [
                                'get order',
                                'edit order',
                                'add order to kitchen',
                                'get order from kitchen',
                                'give order to client',
                                'get payment',
                                'back'
                                ],
        'log out':None
        }
            ]
}

parametres = [
    {
        "name":"users.csv", #0
        "headers":["id","name","email","password","role"]

    } ,
    {
        'name': 'warehouse.csv', #1
        'headers': ['id', 'product', 'measure unit', 'quantity', 'one item price']
    },
    {
        "name":"dishes.csv", #2
        "headers":["dish","product","measure unit","quantity","price"] 
    },
    {
        "name":"orders.csv", #3
        "headers":["id","table","order","quantity","price","status order","status payment"]
    },
    {
        'name': 'invoices.csv', #4
        'headers': ['id','date', 'company name', 'product', 'measure unit', 'quantity', 'one item price', 'total price']
    },
    {
        'name':'distributors.csv', #5
        'headers': ['id', 'company name', 'company address', 'distributor name', 'distributor phone number']
    },
    {
        'name': 'debts.csv', #6
        'headers': ['id', 'date', 'company name', 'unpaid', 'paid', 'income']
    },
    {
        "name":"add_order_to_kitchen.csv", #7
        "headers":["id","table","order","quantity","price","status order","status payment"]
    },
    {
        "name":"orders_to_waiters.csv", #8
        "headers":["id","table","order","quantity","price","status order","status payment"]
    },

    {
        "name":"give_order_to_client.csv", #9
        "headers":["id","table","order","quantity","price","status order","status payment"]
    },
    {
        "name":"paid_orders.csv", #10
        "headers":["id","table","order","quantity","price","status order","status payment"]
    },
    
    {
        "name":"restoraunt_parametres.csv", #-1
        "headers":['id', "tables","salary","margin","comission","budget"]
    }
    ]   



departments['accountant'] = [
    {
        'accountant management': departments['admin'][0]['accountant management'],
        'warehouse management': departments['admin'][0]['warehouse management'],
        'kitchen management': departments['admin'][0]['kitchen management'],
        'waiters management': departments['admin'][0]['waiters management'],
        'log out':None
    }
]
departments['warehouse'] = [
    {
        'warehouse management': departments['admin'][0]['warehouse management'],
        'kitchen management': departments['admin'][0]['kitchen management'],
        'waiters management': departments['admin'][0]['waiters management'],
        'log out':None
    }
]

departments['kitchen'] = [
    {
        
        'kitchen management': departments['admin'][0]['kitchen management'],
        'waiters management': departments['admin'][0]['waiters management'],
        'log out':None
    }
]

departments['waiters'] = [
    {
        'waiters management': departments['admin'][0]['waiters management'],
        'log out':None
    }
]











def tasks_(task,path):

    from creator import file_creator, restoraunt_parametres_changer,user_deleter
    from registrator import users_creator, edit_user
    from kitchen import new_dish, dish_editor_deleter
    from waiters import get_order,edit_order,add_order_to_kitchen,get_orders_from_waiters,give_order_to_waiter_client,get_order_from_kitchen,get_payment,dish_total_price,get_payment
    from finances import get_report_with_date
    
    from distributors import create_new_distributor
    from warehouse import drop_product, get_warehouse_balance
    while True: 
        if task in ["back"]:
            return False
        if task == "create/check necessary files":
            func = file_creator(path)
            print("Task complited\n")
            return False
        elif task == "change tables number":
           func =  restoraunt_parametres_changer(path, "salary")
        elif task == "change salary percent":
             func = restoraunt_parametres_changer(path, "salary")
        elif task == "change margin percent":
            func = restoraunt_parametres_changer(path, "margin")
        elif task == "change commission percent":
            func = restoraunt_parametres_changer(path, "commission")
        elif task == "change budget quantity":
            func = restoraunt_parametres_changer(path, "budget")
        elif task == "add new user":
           func = users_creator(path)
        elif task == "edit user":
            func= edit_user(path)
        elif task == "delete user":
            func = user_deleter(path)
        elif task == "get financial report":
            func, _ = get_report_with_date()
        elif task == "get warehouse balance":
            func, _ = get_warehouse_balance()
        elif task == "calculate dish cost":
            func = dish_total_price(path)
        elif task == "add new distributor":
            func, _ = create_new_distributor()
        elif task == "pay debt":
            from debts import pay_debt, pay_salaries
            func, _ = pay_debt()
        elif task == "pay salaries":
            from debts import pay_salaries
            func, _ = pay_salaries()
        elif task == 'create new invoice':
            from invoices import create_new_invoice
            func, _ = create_new_invoice()
        elif task == "add new product":
            from warehouse import add_product
            func, _ = add_product()
        elif task == "drop product":
            func, _ = drop_product()
        elif task == "add new dish":
            func = new_dish(path)  
        elif task == "edit dish":
            func = dish_editor_deleter(path,"edit",True)
        elif task == "delete dish":
            func = dish_editor_deleter(path,"delete")
        elif task == "get orders":
            func = get_orders_from_waiters(path)
        elif task == "give orders":
            func = give_order_to_waiter_client(path,"Enter id to give order to waiters: ",7,8,"status order","done")
        elif task == "get order":
            func = get_order(path)
        elif task == "edit order":
            func = edit_order(path)
        elif task == "add order to kitchen":
            func = add_order_to_kitchen(path)   
        elif task == "get order from kitchen":
            func = get_order_from_kitchen(path)
        elif task == "give order to client":
            func =  give_order_to_waiter_client(path,"Enter id to give order to costumer: ",8,9,"status payment","inprocess")
        elif task == "get payment":
            func = get_payment(path)
        if not func:
            return False
        



def system_menu_printer(user,text,option=False):
    from user_input_validator import number_validator
    while True:
        if option in ["back","sign out"]:
            return False
        if not option:
            print("Welcome to menu: ")
            department_info =departments[user][0]
        else:
            
            department_info = departments[user][0][option]
        tasks = []

        for index,key in enumerate(department_info):
            print(f"{index+1}. {key}")
            tasks.append(f"{index+1}. {key}")
        while True:
            try:
                user_input = number_validator(f"Choose {text} number: ",int)
                tasks = tasks[user_input-1]
                number , task = tasks.split(".")
                return task.strip()
            except:
                print(f"{text} out of number")
                








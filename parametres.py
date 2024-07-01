
from user_input_validator import number_validator
from printer import role_tasks




departments = {
    'admin': [
        {
        'initiate restorant': [
                            'create/check necessary files',
                            # 'check all files',
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
                                'add new product',
                                'extract product',
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
                                'add order to kitchen',
                                'get order from kitchen',
                                'give order to client'
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
        "headers":["dish","product","measure unit","quantity","price"] #!!!!!!
    },
    {
        "name":"orders.csv", #3
        "headers":["id","table","order","quantity","price","status order","status payment"]
    },
    {
        "name":"menu.csv", #4
        "headers":["dish","price on per unit",]
    },
    {
        'name': 'invoices.csv', #5
        'headers': ['date', 'distributor name', 'product', 'measure unit', 'quantity', 'one item price', 'total price']
    },
    {   
        'name': 'menu_prices.csv', #6
        "headers":["dish","one item price","service Fee(included)"]
    },
    {
        "name":"restoraunt_parametres.csv", #-1
        "headers":["tables","salary","margin","comission","budget"]
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
    while True: 
        if task in ["back"]:
            return False
        if task == "create/check necessary files":
            function =   file_creator(path)
            print("task complited\n")
            return False
        elif task == "change tables number":
           function =  restoraunt_parametres_changer(path, "salary")
        elif task == "change salary percent":
             function = restoraunt_parametres_changer(path, "salary")
        elif task == "change margin percent":
            function = restoraunt_parametres_changer(path, "margin")
        elif task == "change commission percent":
            function = restoraunt_parametres_changer(path, "commission")
        elif task == "change budget quantity":
            function = restoraunt_parametres_changer(path, "budget")
        elif task == "add new user":
           function = users_creator(path)
        elif task == "edit user":
            function= edit_user(path)
        elif task == "delete user":
            function = user_deleter(path)
        elif task == "get financial report":
            pass 
        elif task == "get warehouse balance":
            pass  
        elif task == "calculate dish cost":
            pass 
        elif task == "add new distributor":
            pass  
        elif task == "pay debt":
            pass 
        elif task == "pay salaries":
            pass  
        elif task == "add new product":
            pass  
        elif task == "extract product":
            pass  
        elif task == "drop product":
            pass  
        elif task == "add new dish":
            function = new_dish(path)  
        elif task == "edit dish":
            function = dish_editor_deleter(path,"edit",True)
        elif task == "delete dish":
            function = dish_editor_deleter(path,"delete")
        elif task == "get orders":
            pass 
        elif task == "give orders":
            pass  
        elif task == "get order":
            pass  
        elif task == "add order to kitchen":
            pass 
        elif task == "get order from kitchen":
            pass  
        elif task == "give order to client":
            pass  
        elif task == "get payment":
            pass  
        
        if not function:
            return False
        



def system_menu_printer(user,text,option=False):

    while True:
        if option in ["back","sign out"]:
            return False
        if not option:
            print("welcome to menu: ")
            department_info =departments[user][0]
        else:
            
            department_info = departments[user][0][option]
        tasks = []

        for index,key in enumerate(department_info):
            print(f"{index+1}. {key}")
            tasks.append(f"{index+1}. {key}")
        while True:
            try:
                user_input = number_validator(f"choose {text} number: ",int)
                tasks = tasks[user_input-1]
                number , task = tasks.split(".")
                return task.strip()
            except:
                print(f"{text} out of number")
                







# თარიღი,დისტრიბუტორი, პროდუქტის დასახელება, ზომის ერთეული(კილო,ცალი,ლიტრო), რაოდენობა, ერთეულის ფასი, სრული ფასი
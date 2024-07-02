from crud import read_csv,write_csv,append_csv
from tabulate import tabulate
from parametres import parametres
from registrator import id_creator



def csv_checker(file):
    if not file:
        print("list is empty")
        return False
    return True

def get_order(path):
    from user_input_validator import table_quantity_validator, number_validator,repeat_back
    while True:
        menu = menu_printer(path)
        print(tabulate(menu,headers="keys"))
        data = read_csv(f'{path}/{parametres[3]["name"]}')
        id = id_creator(data)
        table = table_quantity_validator(path)
        dish,one_item_price = get_dish_price(menu)
        quantity = number_validator("Enter dish quantity: ",int)
        price = float(one_item_price) * quantity
        status_order = "in process"
        status_payment = "unpaid"
        data.append({"id":id,"table":table,"order":dish,"quantity":quantity,"price":price,"status order":status_order,"status payment":status_payment})
        write_csv(f'{path}/{parametres[3]["name"]}',data)
        quesiton = repeat_back()
        return quesiton




def edit_order(path):
    from user_input_validator import table_quantity_validator, number_validator,repeat_back
    while True:
        menu = menu_printer(path)
        data = read_csv(f'{path}/{parametres[3]["name"]}')
        if not csv_checker(data):
            break
        print(tabulate(data,headers="keys"))
        user_input = number_validator("Enter order id to edit: ",str)
        for item in data:
            if item["id"] == user_input:
                item["id"] = item["id"]
                item["table"] = table_quantity_validator(path)
                print(tabulate(menu,headers="keys"))
                dish,one_item_price = get_dish_price(menu)
                item["order"] = dish
                quantity = number_validator("Enter dish quantity: ",int)
                item["quantity"] = quantity
                price = float(one_item_price) * quantity
                item["price"] = price
                write_csv(f'{path}/{parametres[3]["name"]}',data)
                quesiton = repeat_back()
                return quesiton



def get_dish_price(menu):
    while True:
        user_input = input("Enter dish: " ).title().strip()
        for dish in menu:
            if user_input ==dish["dish"] :
                return dish["dish"],dish["one item price"]
        print("Enter correct dish")





def dish_total_price(path):
    from user_input_validator import repeat_back
    menu = menu_printer(path)
    print(tabulate(menu,headers="keys"))
    quesiton = repeat_back()
    return quesiton



def menu_printer(path):
    # მენიუს დასაბეჭდად თავის ფასთან და მომსახურების საკომისიოსთან ერთად
    prices = []
    dishes = read_csv(f'{path}/{parametres[2]["name"]}')
    warehouse = read_csv(f'{path}/{parametres[1]["name"]}')
    para = read_csv(f'{path}/{parametres[-1]["name"]}')
    margin = float(para[0]["margin"])
    current_figures = {}
    for dish in dishes:
        total_price = 0
        for item in warehouse:
            if dish["product"] == item["product"]:
                raw_price = float(dish["quantity"]) * float(item["one item price"])
                total_price += raw_price + (raw_price*margin /100)
                current_figures[dish["dish"]] = current_figures.get(dish["dish"],0)+total_price
    for dish in current_figures:
        menu_item = {
            "dish": dish,
            "one item price": round(current_figures[dish],2),

        }
        prices.append(menu_item)
    return prices





def id_validator(data,text):
    
    from user_input_validator import number_validator
    while True:
        user_input = number_validator(text,str)
        for item in data:
            if item["id"] == user_input:
                return user_input
        print("In list there is no such id")




def data_appender(user_input,component,data,order,new_list):
    # ვიყენებ მონაცემების ასააფენდებლად სხვადასხვა ლისტში
    for item in data:
            if item[component] == user_input:
                order.append(item)
            else:
                new_list.append(item)        



def add_order_to_kitchen(path):
    from user_input_validator import repeat_back
    while True:
        data = read_csv(f'{path}/{parametres[3]["name"]}')
        if not csv_checker(data):
            break
        print(tabulate(data,headers="keys"))
        order_to_kitchen = read_csv(f'{path}/{parametres[7]["name"]}')
        user_input = id_validator(data,"Enter id to give order to the kitchen: ")
        new_list=[]
        data_appender(user_input,"id",data,order_to_kitchen,new_list)
        write_csv(f'{path}/{parametres[3]["name"]}',new_list)
        write_csv(f'{path}/{parametres[7]["name"]}',order_to_kitchen)
        quesiton = repeat_back()
        return quesiton
    




def get_orders_from_waiters(path):
    while True:
        from user_input_validator import repeat_back
        order_from_kitchen = read_csv(f'{path}/{parametres[7]["name"]}')
        if not csv_checker(order_from_kitchen):
            break
        print(tabulate(order_from_kitchen,headers="keys"))
        quesiton = repeat_back()
        return quesiton






def give_order_to_waiter_client(path,text,x,y,status_order_payment,status):
    from user_input_validator import repeat_back
    while True:
        order_to_kitchen = read_csv(f'{path}/{parametres[x]["name"]}')
        if not csv_checker(order_to_kitchen):
            break
        print(tabulate(order_to_kitchen,headers="keys"))
        order_to_waiter =  read_csv(f'{path}/{parametres[y]["name"]}')
       
        user_input = id_validator(order_to_kitchen,text)
        for dish in order_to_kitchen:
            if user_input == dish["id"]:
                dish[status_order_payment] = status
        new_list=[]
        data_appender(user_input,"id",order_to_kitchen,order_to_waiter,new_list)
        write_csv(f'{path}/{parametres[x]["name"]}',new_list)
        write_csv(f'{path}/{parametres[y]["name"]}',order_to_waiter)
        quesiton = repeat_back()
        return quesiton





def get_order_from_kitchen(path):
    while True:
        from user_input_validator import repeat_back
        order_to_waiter =  read_csv(f'{path}/{parametres[8]["name"]}')
        if not csv_checker(order_to_waiter):
            break
        print(tabulate(order_to_waiter,headers="keys"))
        quesiton = repeat_back()
        return quesiton

def get_payment(path):
    from user_input_validator import repeat_back
    while True:
        order_to_client =  read_csv(f'{path}/{parametres[9]["name"]}')
        print(tabulate(order_to_client,headers="keys"))
        if not csv_checker(order_to_client):
            break
        pay_orders = read_csv(f'{path}/{parametres[10]["name"]}')

        table_number = table_number_validator(order_to_client)
        for item in order_to_client:
            if item["table"] == table_number:
                item["status payment"] = "paid"
        
        new_list = []

        balance = read_csv(f'{path}/{parametres[-1]["name"]}')
        comission = float(balance[0]["comission"])
        price_to_pay = 0
        
        for price in pay_orders:
            price_to_pay += float(price["price"]) 
        total_price = price_to_pay + price_to_pay*comission/100
        print(f"you have to pay: {total_price}")

        data_appender("paid","status payment",order_to_client,pay_orders,new_list)
        write_csv(f'{path}/{parametres[9]["name"]}',new_list)
        write_csv(f'{path}/{parametres[10]["name"]}',pay_orders)
        
        for item in pay_orders:
            balance["budget"] = float(balance["budget"]) + float(item["price"])
        append_csv(f'{path}/{parametres[-1]["name"]}', balance)
        quesiton = repeat_back()
        return quesiton
  

def table_number_validator(data):
    from user_input_validator import number_validator
    while True:
        user_input = number_validator("Enter table number to pay: ", str)
        for item in data:
            if item["table"] == user_input:
                return user_input
            
        print("There is not such table")

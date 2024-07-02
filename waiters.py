from crud import read_csv,write_csv
from tabulate import tabulate
from parametres import parametres
from registrator import id_creator



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










def menu_printer(path):
    # მენიუს დასაბეჭდად თავის ფასთან და მომსახურების საკომისიოსთან ერთად
    prices = []
    dishes = read_csv(f'{path}/{parametres[2]["name"]}')
    warehouse = read_csv(f'{path}/{parametres[1]["name"]}')
    para = read_csv(f'{path}/{parametres[-1]["name"]}')
    margin = float(para[0]["margin"])
    comission = float(para[0]["comission"])
    current_figures = {}
    for dish in dishes:
        total_price = 0
        for item in warehouse:
            if dish["product"] == item["product"]:
                raw_price = float(dish["quantity"]) * float(item["one item price"])
                total_price += raw_price + (raw_price*margin /100) + (raw_price*comission/100)
                current_figures[dish["dish"]] = current_figures.get(dish["dish"],0)+total_price
    

    for dish in current_figures:
        menu_item = {
            "dish": dish,
            "one item price": round(current_figures[dish],2),
            "service Fee(included)": round(current_figures[dish]*comission/100 ,2)
        }
        prices.append(menu_item)
    return prices





# def give_order_kitchen(path):
#     # მიცეს სამზარეილოს შეკვეთების სია
#     from user_input_validator import repeat_back
#     while True:
#         menu = read_csv(f'{path}/{parametres[3]["name"]}')
#         printer = []
#         for dish in menu:
#             if dish["status order"] != "done":
#                 printer.append(dish)
#         print(tabulate(printer,headers="keys"))
#         quesiton = repeat_back()
#         return quesiton

# def add_order_to_kitchen(path):
#     from user_input_validator import repeat_back
#     while True:
#         menu = read_csv(f'{path}/{parametres[3]["name"]}')
#         done_order = read_csv(f'{path}/{parametres[6]["name"]}')
#         for dish in menu:
#             if dish["status order"] == "done":
#                 done_order.append(dish)
#         write_csv(f'{path}/{parametres[6]["name"]}',menu)
#         print(tabulate(done_order,headers="keys"))
#         quesiton = repeat_back()
#         return quesiton       



# def get_order_from_kitchen(path):
#     from user_input_validator import repeat_back
#     while True:
#         menu = read_csv(f'{path}/{parametres[3]["name"]}')
#         done_order = read_csv(f'{path}/{parametres[6]["name"]}')
#         for dish in menu:
#             if dish["status order"] == "done":
#                 done_order.append(dish)
#         write_csv(f'{path}/{parametres[6]["name"]}',menu)
#         print(tabulate(done_order,headers="keys"))
#         quesiton = repeat_back()
#         return quesiton    
    


# def give_order_to_client(path):
#     while True:
#         menu = read_csv(f'{path}/{parametres[3]["name"]}')
#         user_input = input("which table are you giving order? \n ")
     

# 'get orders',
# 'give orders',
# 'back'

# 'get order',
#  edit order
# 'add order to kitchen',
# 'get order from kitchen',
# 'give order to client'
# 'get payment',
# 'back'

def id_validator(data,text):
    
    from user_input_validator import number_validator
    while True:
        user_input = number_validator(text,str)
        for item in data:
            if item["id"] == user_input:
                return user_input
        print("In list there is no such id")




def data_appender(user_input,data,order,new_list):
    # ვიყენებ მონაცემების ასააფენდებლად სხვადასხვა ლისტში
    for item in data:
            if item["id"] == user_input:
                order.append(item)
            else:
                new_list.append(item)        



def add_order_to_kitchen(path):
    from user_input_validator import repeat_back
    while True:
        data = read_csv(f'{path}/{parametres[3]["name"]}')
        print(tabulate(data,headers="keys"))
        order_to_kitchen = read_csv(f'{path}/{parametres[7]["name"]}')
        user_input = id_validator(data,"Enter id to give order to the kitchen: ")
        new_list=[]
        data_appender(user_input,data,order_to_kitchen,new_list)
        write_csv(f'{path}/{parametres[3]["name"]}',new_list)
        write_csv(f'{path}/{parametres[7]["name"]}',order_to_kitchen)
        quesiton = repeat_back()
        return quesiton
    
# add_order_to_kitchen("restorauntParametres")



def get_orders_from_waiters(path):
    from user_input_validator import repeat_back

    order_from_kitchen = read_csv(f'{path}/{parametres[7]["name"]}')
    print(tabulate(order_from_kitchen,headers="keys"))
    quesiton = repeat_back()
    return quesiton





# def give_order_to_waiter(path):
#     while True:     
#         menu = read_csv(f'{path}/{parametres[3]["name"]}')
#         print(tabulate(menu,headers="keys"))
#         user_input = number_validator("enter dish id: ",str)
#         for dish in menu:
#             if user_input == dish["id"]:
#                 dish["status order"] = "done"
#         write_csv(f'{path}/{parametres[3]["name"]}',menu)
#         quesiton = repeat_back()
#         return quesiton    

def give_order_to_waiter(path):
    from user_input_validator import repeat_back
    while True:
        order_to_kitchen = read_csv(f'{path}/{parametres[7]["name"]}')
        print(tabulate(order_to_kitchen,headers="keys"))
        order_to_waiter =  read_csv(f'{path}/{parametres[8]["name"]}')
       
        user_input = id_validator(order_to_kitchen,"Enter id to give order to waiters: ")
        for dish in order_to_kitchen:
            if user_input == dish["id"]:
                dish["status order"] = "done"
        new_list=[]
        data_appender(user_input,order_to_kitchen,order_to_waiter,new_list)
        write_csv(f'{path}/{parametres[7]["name"]}',new_list)
        write_csv(f'{path}/{parametres[8]["name"]}',order_to_waiter)
        quesiton = repeat_back()
        return quesiton


# give_order_to_waiter("restorauntParametres")

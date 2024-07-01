from crud import read_csv,write_csv
from tabulate import tabulate
from parametres import parametres
from registrator import id_creator



# "headers":["id","table","order","quantity","price","status order","status payment"]
def get_order(path):
    from user_input_validator import table_quantity_validator, number_validator,repeat_back
    while True:
        menu = menu_printer(path)
        print(tabulate(menu,headers="keys"))
        data = read_csv(f'{path}/{parametres[3]["name"]}')
       
        id = id_creator(data)
        table = table_quantity_validator(path)
        dish,one_item_price = get_dish_price(menu)
        quantity = number_validator("enter dish quantity: ",int)
        price = float(one_item_price) * quantity
        status_order = "in process"
        status_payment = "unpaid"
        data.append({"id":id,"table":table,"order":dish,"quantity":quantity,"price":price,"status order":status_order,"status payment":status_payment})
        write_csv(f'{path}/{parametres[3]["name"]}',data)
        quesiton = repeat_back()
        return quesiton



def get_dish_price(menu):
    while True:
        user_input = input("Enter dish: " )
        for dish in menu:
            if user_input ==dish["dish"] :
                return dish["dish"],dish["one item price"]
        print("enter correct dish")










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





def give_order_kitchen(path):
    # მიცეს სამზარეილოს შეკვეთების სია
    from user_input_validator import repeat_back
    while True:
        menu = read_csv(f'{path}/{parametres[3]["name"]}')
        printer = []
        for dish in menu:
            if dish["status order"] != "done":
                printer.append(dish)
        print(tabulate(printer,headers="keys"))
        quesiton = repeat_back()
        return quesiton

def add_order_to_kitchen(path):
    from user_input_validator import repeat_back
    while True:
        menu = read_csv(f'{path}/{parametres[3]["name"]}')
        done_order = read_csv(f'{path}/{parametres[6]["name"]}')
        for dish in menu:
            if dish["status order"] == "done":
                done_order.append(dish)
        write_csv(f'{path}/{parametres[6]["name"]}',menu)
        print(tabulate(done_order,headers="keys"))
        quesiton = repeat_back()
        return quesiton       



def get_order_from_kitchen(path):
    from user_input_validator import repeat_back
    while True:
        menu = read_csv(f'{path}/{parametres[3]["name"]}')
        done_order = read_csv(f'{path}/{parametres[6]["name"]}')
        for dish in menu:
            if dish["status order"] == "done":
                done_order.append(dish)
        write_csv(f'{path}/{parametres[6]["name"]}',menu)
        print(tabulate(done_order,headers="keys"))
        quesiton = repeat_back()
        return quesiton    
    


def give_order_to_client(path):
    while True:
        menu = read_csv(f'{path}/{parametres[3]["name"]}')
        user_input = input("which table are you giving order? \n ")

from crud import read_csv,write_csv
from tabulate import tabulate
from parametres import parametres
from registrator import id_creator



# "headers":["id","table","order","quantity","price","status order","status payment"]
def get_order(path):
    from user_input_validator import table_quantity_validator, number_validator

    menu = menu_printer(path)
    
    data = read_csv(f'{path}/{parametres[3]["name"]}')
    # menu_printer(path)
    id = id_creator(data)
    table = table_quantity_validator(path)
    dish,one_item_price = get_dish_price(menu)
    quantity = number_validator("enter dish quantity: ",int)
    price = float(one_item_price) * quantity
    status_order = ""
    status_payment = ""


def get_dish_price(menu):
    while True:
        user_input = input("Enter dish: " ).title()
        for dish in menu:
            if dish["dish"] == user_input:
                return dish["dish"],dish["one item price"]











def menu_printer(path):
    # მენიუს დასაბეჭდად თავის ფასთან და მომსახურების საკომისიოსთან ერთად
    prices = read_csv(f'{path}/{parametres[6]["name"]}')
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
    write_csv(f'{path}/{parametres[6]["name"]}',prices)
    
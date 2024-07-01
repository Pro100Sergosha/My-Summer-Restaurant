from crud import read_csv,write_csv
from parametres import parametres
from registrator import name_validator
from user_input_validator import number_validator,repeat_back
from tabulate import tabulate

def new_dish(path):
    # კერძის შესაქმენლად ვიყენებ
    # data = read_csv(f'{path}/{parametres[2]["name"]}')
    dish_name = name_validator("enter dish name: ")
    while True:
        data = read_csv(f'{path}/{parametres[2]["name"]}')
        temp_dict ={"dish":dish_name}
        temp_dict.update(dish_registrator(path))
        data.append(temp_dict)
        write_csv(f'{path}/{parametres[2]["name"]}',data)
        quesiton = repeat_back()
        return quesiton
        






def dish_registrator(path):
    # მომხმარებლისგან ინფოქრმაციის წამოსაღებად ვიყენებ
    ingredient = product_getter(path)
    unit = unit_getter(path,ingredient)
    quantity = quantity_getter(path,ingredient)
    price= product_price_getter(ingredient,quantity,path)
    temp_dict= {"product":ingredient,"measure unit":unit,"quantity":quantity,"price":price}
    return temp_dict

def product_price_getter(ingredient,quantity,path):
    # კონკრეტული ინგრედიენტის ფასის დასადგენად ვიყენებ ამ ფუნქციას
    warehouse = read_csv(f'{path}/{parametres[1]["name"]}')
    for item in warehouse:
        if item["product"] == ingredient:
            price =  round(float(item["one item price"])*quantity,2)
            return price


def product_getter(path):
    # დაადგინოს არის თუ არა პროდუქტი პროდუქტების ლისტში
    products = read_csv(f'{path}/{parametres[1]["name"]}')
    printer = [product for product in products]
    print(tabulate(printer,headers="keys"))
    while True:
        ingredient = name_validator("enter ingredient: ").title()
        for product in products:
            if product["product"] == ingredient:
                return ingredient
        print("in warehouse is not such ingredient")    



def quantity_getter(path,ingredient):
    # დაადგინოს არის თუ არა პროდუქტის რაოდენობა შეყვანილ რაოდენობაზე ნაკლები
    products = read_csv(f'{path}/{parametres[1]["name"]}')
    printer = [product for product in products if product["product"] == ingredient]
    # for product in products:
    #     if product["product"] == ingredient:
    #         printer.append(product)
    print(tabulate(printer,headers="keys"))
    while True:
        for product in products:
            if product["product"] == ingredient:
                quantity = number_validator("Enter quantity: ", float)
                if quantity <= float(product["quantity"]) and quantity > 0:
                    return quantity
                print("more than quantity")



def unit_getter(path,ingredient):
    # შესაბაბისი საზომი ერთეული რომ თავისით წამოიღოს
    products = read_csv(f'{path}/{parametres[1]["name"]}')
    for product in products:
        if product["product"] == ingredient:
                print(f"product measure unit is {product['measure unit']}")
                return product['measure unit']
        


# def user_deleter(path):
#     while True:
#         data = read_csv(f'{path}/{parametres[0]["name"]}')
#         user_printer(data)
#         user_input =  number_validator("enter id to delete: ",str)
#         if int(user_input) > len(data):
#             continue
#         delete = lambda d: d['id'] == user_input
#         delete_list = [i for i in data if not delete(i)]
#         # print(delete_list)
#         write_csv(f'{path}/{parametres[0]["name"]}',delete_list)
#         user_printer(data)
#         quesiton = repeat_back()
#         if not quesiton:
#             return False


def dish_editor_deleter(path,txt,option=False):
    data = read_csv(f'{path}/{parametres[2]["name"]}')
    print(tabulate(data,headers="keys"))
    while True:
        user_input = input(f"Enter dish to {txt}: ")
        delete = lambda d: d["dish"] == user_input
        if any(delete(d) for d in data):
            delete_list = [i for i in data if not delete(i)]
            if option:
                dish_name = name_validator("enter dish name: ")
                temp_dict ={"dish":dish_name}
                temp_dict.update(dish_registrator(path))
                delete_list.append(temp_dict)
            print(tabulate(delete_list,headers="keys"))
            write_csv(f'{path}/{parametres[2]["name"]}',delete_list)
            quesiton = repeat_back()
            return quesiton
        else:
            print("dish isnot in list")



 
            





def menu_printer(path):
    dishes = read_csv(f'{path}/{parametres[2]["name"]}')
    warehouse = read_csv(f'{path}/{parametres[1]["name"]}')
    para = read_csv(f'{path}/{parametres[-1]["name"]}')

    current_figures = {}
    for dish in dishes:
        total_price = 0
        for item in warehouse:
            if dish["product"] == item["product"]:
                raw_price = float(dish["quantity"]) * float(item["one item price"])
                total_price += raw_price + (raw_price*float(para[0]["margin"])/100) + (raw_price*float(para[0]["comission"])/100)
                current_figures[dish["dish"]] = current_figures.get(dish["dish"],0)+total_price
    print(current_figures)

    printer = [{"dish":item,"one item price":current_figures[item],"Service Fee(included)":float(current_figures[item])*float(para[0]["comission"])/100} for item in current_figures]
    # for item in current_figures:
    #     printer.append({"dish":item,"one item price":current_figures[item]}) 
    print(tabulate(printer,headers="keys"))
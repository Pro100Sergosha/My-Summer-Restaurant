import os
import csv
from parametres import parametres
from user_input_validator import number_validator, repeat_back
from registrator import super_user_ceator
from printer import user_printer


def folder_path():
    parent_dir  = os.getcwd()
    directory = "restorauntParametres"
    path = os.path.join(parent_dir,directory)
    if not os.path.isdir(path):
        os.mkdir(path)
    return path



def file_creator(path):
    for index in parametres :
        check_file = os.path.exists(f"{path}/{index['name']}")
        if not check_file:
            headers = index["headers"]
            with open(f"{path}/{index['name']}", "w") as file:
                write = csv.DictWriter(file,fieldnames=headers)
                write.writeheader()
    return False            

def file_info(path):
    # ფაილების შექმნა მაქვს ცალკე ფუქციად გატანილი, რადგან რამდენიმეჯერ მჭირდება გამოძახება
    file_creator(path)
    from crud import write_csv, read_csv
    users_info = read_csv(f'{path}/{parametres[0]["name"]}')
    return users_info


def create_admin(path):
    from crud import write_csv, read_csv
    print()
    print("Register to system")
    users = super_user_ceator()
    write_csv(f'{path}/{parametres[0]["name"]}',users)
    print("You are registered\n")



def restoraunt_para_creator():
    param = []

    tables = number_validator("enter table quantity: ",int)
    salary = number_validator("enter salary: ",int)
    margin = number_validator("enter margin percent: ",int)
    comission = number_validator("enter comissiont percent: ",int)
    budget = number_validator("enter budget: ", int)
    param.append({"tables":tables,"salary":salary,"margin":margin,"comission":comission,"budget":budget})
  
    return param





def restoraunt_parametres_changer(path,param):
    from crud import write_csv, read_csv
    while True:
        change = read_csv(f'{path}/{parametres[-1]["name"]}')
        print(f'{param} value: {change[0][param]} ')
        user_input = number_validator(f"change {param} value: ",int)
        change[0][param] = user_input
        write_csv(f'{path}/{parametres[-1]["name"]}',change)
        quesiton = repeat_back()
        return quesiton







def user_deleter(path):
    from crud import write_csv, read_csv
    while True:
        data = read_csv(f'{path}/{parametres[0]["name"]}')
        user_printer(data)
        user_input =  number_validator("enter id to delete: ",str)
        if int(user_input) > len(data):
            continue
        delete = lambda d: d['id'] == user_input
        delete_list = [i for i in data if not delete(i)]
        write_csv(f'{path}/{parametres[0]["name"]}',delete_list)
        user_printer(data)
        quesiton = repeat_back()
        return quesiton


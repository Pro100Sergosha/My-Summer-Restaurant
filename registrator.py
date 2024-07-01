from crud import read_csv,write_csv
import re
import string
import bcrypt 
from user_input_validator import yes_no,repeat_back,number_validator
from parametres import parametres
from getpass import getpass
import sys
from printer import user_printer

def super_user_ceator():
    user= []
    # "id","name","email","password","role"
    id = 1 
    name = name_validator("Enter your name: ")
    email = email_validator()
    password = password_validator()
    role = "admin"
    user.append({"id":id,"name":name,"email":email,"password":password.decode("'utf-8'"), "role":role})
    return user


def users_creator(path):
    while True:
        users = read_csv(f'{path}/{parametres[0]["name"]}')
        
        id = id_creator(users)
        name = name_validator("Enter your name: ")
        email = email_validator()
        password = password_validator()
        role = role_validator()
        users.append({"id":id,"name":name,"email":email,"password":password.decode("'utf-8'"), "role":role})
        write_csv(f'{path}/{parametres[0]["name"]}',users)
        annswer = repeat_back()
        return annswer



def edit_user(path):
    while True:
        users = read_csv(f'{path}/{parametres[0]["name"]}')
        user_printer(users)
        user_input = number_validator("Enter id to edit: ",str)
        for line in users:
            if user_input == line["id"]:
                line["name"] = name_validator("Enter your name: ")
                line["email"] = email_validator()
                line["password"] = password_validator()
                line["role"] = role_validator()
        write_csv(f'{path}/{parametres[0]["name"]}',users)    
        user_printer(users)
        annswer = repeat_back()
        return annswer


def id_creator(data):
    # data = read_csv(f'{path}/{parametres[x]["name"]}')
    try:
        new_id = int(data[-1]["id"])+1
        return new_id
    except (IndexError, KeyError):
        return 1


def name_validator(txt):
    while True:
        user_input = input(txt)
        if user_input:
            return user_input
        print("Enter correct name")

# name_validator("asdasd: ")


def email_validator():
    pattern = "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    while True:
        user_input = input("enter email or just press enter: ").strip()
        if user_input == "":
            return user_input
        elif re.match(pattern,user_input):
            return user_input
        print("Enter correct email or just press enter")

# print(email_validator("enter your email: "))

def password_validator():
    while True:
        password = getpass(prompt = "Enter your new password: ")
        re_password = getpass(prompt ="Re enter your password: ")
        if password == re_password:
            if (any( i in string.punctuation for i in password) and 
                any(i in string.digits for i in password) and 
                any(i in string.ascii_lowercase for i in password) and 
                any(i in string.ascii_uppercase for i in password) and 
                len(password) >=8):
                print("strong password")
                return hashing_password(password)
            else:
                print("Your password is weak.")
                if yes_no("would like to save it? (yes/no) ",True,False):
                    return hashing_password(password)
                else:
                    continue
        else:print("Passwords don't match please re enter your password " ) 


def role_validator(): 
    while True:
        user_input = input("choose role: \n1.admin\n2.accountant\n3.warehouse\n4.kitchen\n5.waiters\nEnter number: ")
        if user_input == "1":
            return "admin"
        elif user_input == "2":
            return "accountant"
        elif user_input == "3":
            return "warehouse"
        elif user_input == "4":
            return "kitchen"
        elif user_input == "5":
            return "waiters"
        else:
            print("\nEnter correct number")




def hashing_password(password): 
    # პაროლს კრიპტავს
    salt = bcrypt.gensalt() 
    hash = bcrypt.hashpw(password.encode('utf-8') , salt) 
    return hash

# password = hashing_password("asd")
# print(password)


def encoding_password(user_password,password):
    # დაკრიპტული პაროლის და იუზერისგან მოსული პაროლის შესადარებლად
    userBytes = user_password.encode('utf-8') 
    result = bcrypt.checkpw(userBytes, password.lstrip("b'").rstrip("'").encode('utf-8')) 
    return result

# print(encoding_password(b'$2b$12$yPDlH1sTnCn7Dwe31aSBqOmU/aTxRCazqVtOLndifJR1dKNdH7i3i',"enter password: " ))


def login_user(data):

    while True:
        user_name = name_validator("Enter your name: ")
        user_password = getpass(prompt = "Enter your password: ")
        for i in data:
            if encoding_password(user_password,i["password"]) and user_name == i["name"]  :
                    print("login successful")
                    return i["role"]
            
        print("wrong user name or password")        


def login_user_role_getter(users_info):
        yes_or_no = yes_no("Would you like to sign in? (yes/no) ",True,False)    
        if yes_or_no:
            role =  login_user(users_info)
            return role
        else:
            sys.exit("goobye")

from crud import read_csv



def yes_no(text,x,z):
    while True:
        user = input(text).lower().strip()
        if user == "yes":
            return x
        elif user == "no":
            return z
        else:
            print("Enter only yes or no")


def number_validator(text,type):
    while True:
        user_input = input(text).strip()
        if user_input.isdigit():
            return type(user_input)
        print ("enter only numbers")




def repeat_back():
    while True:
        user_input = input("what would you like to do? (repeat/back): ").strip().lower()
        if user_input == "repeat":
            return True
        elif user_input == "back":
            return False
        else:
            print("invalid input")  



def table_quantity_validator(path):
    from parametres import parametres


    data = read_csv(f'{path}/{parametres[-1]["name"]}')
    while True:
        try:
            user_input = int(input(f"table quantity: {data[0]['tables']}\nEnter table number: "))
            if user_input > int(data[0]["tables"]):
                print("more than quantity")
            else:
                question = repeat_back()
                if not question:
                    return user_input
        except:
            print("Enter number")




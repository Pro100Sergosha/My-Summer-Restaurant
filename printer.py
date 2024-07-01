import tabulate

def role_tasks(departments,role,x):
    warehouse_tasks = []
    for k, v in departments['admin'][0].items():
         if k not in list(departments['admin'][0].keys())[:x]:
             warehouse_tasks.append({k: v})
    departments[role] = warehouse_tasks
    
    


def user_printer(data):
    modified_users = []
    for user in data:
        modified_users.append({"id":user["id"],"name":user["name"],"email":user["email"], "role":user["role"]})
    print(tabulate.tabulate(modified_users,headers="keys"))



# asd =[{'id': '1', 'name': 'dato', 'email': '', 'password': '$2b$12$c362zLZI.iK5hqtu5Mlt5eYRyvh0w.w3jI9m6JCB9k9YG6JVxkl12', 'role': 'admin'}, {'id': '2', 'name': 'gio', 'email': '', 'password': '$2b$12$EonI32uV3RQOogGnXcjJZ.dtnGUOotuAGLrAHWRXIy7/xKOKGmZZ6', 'role': 'kitchen'}, {'id': '3', 'name': 'giorgi', 'email': '', 'password': '$2b$12$Tzr/IvnB2lJc4I7mZdQzJedoqyBjkVgYn9x3I48XqnbMghySD7yrS', 'role': 'accountant'}]
# for i in asd:
#     print(i["id"])
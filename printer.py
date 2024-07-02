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



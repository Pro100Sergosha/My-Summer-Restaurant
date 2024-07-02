

from parametres import parametres, system_menu_printer, tasks_



def main():
    while True: 
        try:
            from crud import write_csv, read_csv
            from creator import folder_path,restoraunt_para_creator,file_info, create_admin
            from registrator import login_user_role_getter
            print("Welcome to application!")
            path = folder_path()
            users_creator = file_info(path)

        
        

            if not users_creator:  
                create_admin(path)
            restourant_par = read_csv(f'{path}/{parametres[-1]["name"]}')
            if not restourant_par:
                print("Enter restouraunt parametres")
                data = restoraunt_para_creator()
                write_csv(f'{path}/{parametres[-1]["name"]}',data)
                print()
            users_info = read_csv(f'{path}/{parametres[0]["name"]}')
            role = login_user_role_getter(users_info)
            while True:
                option = system_menu_printer(role,"option")
                if option == "log out":
                    main()
                while True:
                    task = system_menu_printer(role,"task",option)
                    if  task == "back":
                        break
                    while True:
                        functions = tasks_(task,path)
                        if not functions:
                            break 
        except EOFError:
            print("System shut down")
        except:
            from creator import file_creator
            file_creator(path)
            pass

if __name__=="__main__":
    main()
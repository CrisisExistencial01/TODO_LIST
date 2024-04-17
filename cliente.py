BASE_URL = 'http://50.16.235.247'
def CC_create_user(user_id):
    url = BASE_URL + 'CC_create_user'
    data = {'CC_user_id': user_id}
    response = requests.post(url, json=data)
    return response.json()

def CC_create_task(user_id, title, description):
    url = BASE_URL + f'CC_create_task/{user_id}'
    data = {'CC_title': title, 'CC_description': description}
    response = requests.post(url, json=data)
    return response.json()

def CC_list_tasks(user_id):
    url = BASE_URL + f'CC_list_tasks/{user_id}'
    response = requests.get(url)
    return response.json()

def CC_update_task(user_id, task_index, title, description):
    url = BASE_URL + f'CC_update_task/{user_id}/{task_index}'
    data = {'CC_title': title, 'CC_description': description}
    response = requests.put(url, json=data)
    return response.json()

def CC_delete_task(user_id, task_index):
    url = BASE_URL + f'CC_delete_task/{user_id}/{task_index}'
    response = requests.delete(url)
    return response.json()

if __name__ == '__main__':
    user_id = input("Ingrese el ID del usuario: ")
    CC_create_user(user_id)
   
    while True:
        print("\nSeleccione una opción:")
        print("1. Crear tarea")
        print("2. Listar tareas")
        print("3. Actualizar tarea")
        print("4. Eliminar tarea")
        print("5. Salir")

        choice = input("Ingrese el número de la opción deseada: ")

        if choice == '1':
            title = input("Ingrese el título de la tarea: ")
            description = input("Ingrese la descripción de la tarea: ")
            CC_create_task(user_id, title, description)
            print("Tarea creada exitosamente.")
        elif choice == '2':
            tasks = CC_list_tasks(user_id)
            print("Lista de tareas:")
            for i, task in enumerate(tasks):
                print(f"Índice: {i}, Título: {task['title']}, Descripción: {task['description']}")
        elif choice == '3':
            task_index = int(input("Ingrese el índice de la tarea que desea actualizar: "))
            title = input("Ingrese el nuevo título de la tarea: ")
            description = input("Ingrese la nueva descripción de la tarea: ")
            CC_update_task(user_id, task_index, title, description)
            print("Tarea actualizada exitosamente.")
        elif choice == '4':
            task_index = int(input("Ingrese el índice de la tarea que desea eliminar: "))
            CC_delete_task(user_id, task_index)
            print("Tarea eliminada exitosamente.")
        elif choice == '5':
            print("Saliendo del programa...")
            break
        else:
            print("Opción inválida. Por favor, ingrese un número del 1 al 5.")


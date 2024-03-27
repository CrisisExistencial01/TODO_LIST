import requests
import json
import sys

class Client:
    def __init__(self):
        self.CC_url = 'http://50.16.235.247:8081/todos'
        self.CC_todos = self.get()

    def get(self):
        try:
            CC_response = requests.get(self.CC_url)
            return CC_response.json()
        except requests.exceptions.RequestException as e:
            print("Error al obtener las tareas:", e)
            return None
    def get_todos(self):
        formatted_tasks = [f'{task["task"]}, id: {task["ID"]}' for task in self.CC_todos]
        return formatted_tasks

    def add_task(self):
        description = input("Ingrese la descripción de la tarea: ")
        CC_todo_id = len(self.CC_todos) + 1 # ID de la nueva tarea es el siguiente al último
        CC_data = {"ID":CC_todo_id, "task":description}
        self.CC_todos.append(CC_data)
        CC_response = self.post(CC_data)
        if CC_response is not None:
            print("Tarea creada exitosamente:")

    def update_task(self):
        task_id = input("Ingrese el ID de la tarea que desea actualizar: ")
        if not task_id.isdigit():
            print("ID inválido. Por favor, intenta de nuevo.")
            return None

        description = input("Ingrese la nueva descripción de la tarea: ")
        CC_data = {"ID":task_id, "task":description}
        CC_response = self.put(task_id, CC_data) # self.put(CC_data) si se quiere enviar el ID         
        if CC_response is not None:
            print("Tarea actualizada exitosamente:")
            self.CC_todos = self.get()
    def delete_task(self):
        # ingresa un id, lo valida y lo envia a la funcion delete
        task_id = input("Ingrese el ID de la tarea que desea eliminar: ")
        if not task_id.isdigit():
            print("ID inválido. Por favor, intenta de nuevo.")
            return None

        CC_response = self.delete(task_id)

        if CC_response is not None:
            print("Tarea eliminada exitosamente")
            self.CC_todos = self.get()

    def menuText(self):
        print("1. Ver todas las tareas")
        print("2. Crear una nueva tarea")
        print("3. Actualizar una tarea")
        print("4. Borrar una tarea")
        print("0. Salir")
        return input("Ingresa tu elección: ")

    def menu(self):
        while True:
            choice = self.menuText()
            if choice == '1':
                for i in self.get_todos():
                    print(i)
            elif choice == '2':
                self.add_task()
            elif choice == '3':
                self.update_task()
            elif choice == '4':
                self.delete_task()
            elif choice == '0':
                break
            else:
                print("Opción inválida. Por favor, intenta de nuevo.")
        print("¡Adiós!")

    def post(self, CC_data):
        try:
            CC_response = requests.post(self.CC_url, json=CC_data)
            return CC_response.json()
        except requests.exceptions.RequestException as e:
            print("Error al crear la tarea:", e)
            return None

    def put(self, task_id, CC_data):
        try:
            update_CC_url = f"{self.CC_url}/{task_id}"
            CC_response = requests.put(update_CC_url, json=CC_data)
            return CC_response.json()
        except requests.exceptions.RequestException as e:
            print("Error al actualizar la tarea:", e)
            return None

    def delete(self, task_id):
        try:
            delete_CC_url = f"{self.CC_url}/{task_id}"
            CC_response = requests.delete(delete_CC_url)
            return CC_response.json()
        except requests.exceptions.RequestException as e:
            print("Error al eliminar la tarea:", e)
            return None

app = Client()
app.menu()


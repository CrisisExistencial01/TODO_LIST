import requests

class Client:
    def __init__(self):
        self.url = 'http://50.16.235.247:8081/todos'
        self.ToDos = self.get()

    def get(self):
        try:
            response = requests.get(self.url)
            return response.json()
        except requests.exceptions.RequestException as e:
            print("Error al obtener las tareas:", e)
            return None

    def get_todos(self):
        formatted_tasks = [f'{task["task"]} {task["ID"]}' for task in self.ToDos]
        return formatted_tasks

    def add_task(self):
        description = input("Ingrese la descripción de la tarea: ")
        todo_id = len(self.ToDos) + 1  # Genera un ID único para la nueva tarea
        data = {"ID": todo_id, "task": description}
        self.ToDos.append(data)
        response = self.post(data)
        if response is not None:
            print("Tarea creada exitosamente:", response)

    def update_task(self):
        task_id = int(input("Ingrese el ID de la tarea que desea actualizar: "))
        description = input("Ingrese la nueva descripción de la tarea: ")

        data = {'ID': task_id, 'task': description}  # ID de la tarea a actualizar y la nueva descripción de la tarea
        response = self.put(task_id, data)
        if response is not None:
            print("Tarea actualizada exitosamente:", response)

    def delete_task(self):
        task_id = input("Ingrese el ID de la tarea que desea eliminar: ")
        response = self.delete(task_id)
        if response is not None:
            print("Tarea eliminada exitosamente")

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

    def post(self, data):
        try:
            response = requests.post(self.url, json=data)
            return response.json()
        except requests.exceptions.RequestException as e:
            print("Error al crear la tarea:", e)
            return None

    def put(self, task_id, data):
        try:
            update_url = f"{self.url}/{task_id}"
            response = requests.put(update_url, json=data)
            return response.json()
        except requests.exceptions.RequestException as e:
            print("Error al actualizar la tarea:", e)
            return None

    def delete(self, task_id):
        try:
            delete_url = f"{self.url}/{task_id}"
            response = requests.delete(delete_url)
            return response.json()
        except requests.exceptions.RequestException as e:
            print("Error al eliminar la tarea:", e)
            return None

app = Client()
app.menu()


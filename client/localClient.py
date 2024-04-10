import requests
import json
class LocalClient:
    def __init__(self):
        self.user = None
        self.url = "http://50.16.235.247:8081"
    def verificarConexion(self):
        print("Verificando conexión con el servidor...")
        try:
            response = requests.get(self.url, timeout=3) # timeout=5 indica que la conexión se considera fallida si no se recibe respuesta en 5 segundos
            return True
        except requests.exceptions.RequestException:
            return False
    def get(self, path):
        response = requests.get(self.url + path)
        return response.json()["msg"]

    def post(self, path, data):
        response = requests.post(self.url + path, json=data)
        msg = response.json()["msg"]
        return msg

    def put(self, path, data):
        response = requests.put(self.url + path, json=data)
        return response.json()["msg"]

    def delete(self, path):
        response = requests.delete(self.url + path)
        return response.json()["msg"]

    def login(self, rut, password):
        self.user = rut
        data = {"user": rut, "password": password}
        path = "/login"
        return self.post(path, data)

    def logout(self):
        path = "/logout"
        return self.get(path)

    def register(self, rut, password):
        user = {"rut": rut, "password": password}
        path = "/register"
        return self.post(path, user)

    def get_todos(self):
        path = f"/{self.user}/todos"
        return self.get(path)

    def add_todo(self, title, description):
        task = {"user": self.user, "title": title, "description": description}
        path = f"/{self.user}/todos"
        return self.post(path, task)

    def update_todo(self, task_id, title, status, description):
        task = {"title": title, "status": status, "description": description}
        path = f"/{self.user}/todos/{task_id}"
        return self.put(path, task)

    def delete_todo(self, task_id):
        path = f"/{self.user}/todos/{task_id}"
        return self.delete(path)
class menu:
    def __init__(self):
        self.client = LocalClient()
        self.user = None
    def login(self):
        rut = input("Ingrese su rut: ")
        password = input("Ingrese su contraseña: ")
        response = self.client.login(rut, password)
        print(response) # Imprime "Logged in successfully" o "Invalid credentials"
        if response == "Logged in successfully":
            self.user = rut
    def register(self):
        rut = input("Ingrese su rut: ")
        password = input("Ingrese su contraseña: ")
        response = self.client.register(rut, password)
        print(response) # Imprime "User created successfully" o "User already exists"
    def logout(self):
        response = self.client.logout()
        print(response) # Imprime "Logged out successfully"
    def menuText(self):
        print("1. Iniciar sesión")
        print("2. Registrarse")
        print("3. Cerrar sesión")
        print("4. Salir")
    def printTodos(self):
        todos = self.client.get_todos()
        print("Tareas:")
        for task in todos:
            print(f"{task['id']}. {task['title']} ({task['status']})")
    def menuUser(self):
        while True:
            print("1. Agregar tarea")
            print("2. Editar tarea")
            print("3. Eliminar tarea")
            print("0. Volver")
            option = input("Seleccione una opción: ")
            if option == "1":
                title = input("Ingrese el título de la tarea: ")
                description = input("Ingrese la descripción de la tarea: ")
                response = self.client.add_todo(title, description)
                print(response)
            elif option == "2":
                task_id = input("Ingrese el id de la tarea a editar: ")
                title = input("Ingrese el nuevo título de la tarea: ")
                status = input("Ingrese el nuevo estado de la tarea: ")
                description = input("Ingrese la nueva descripción de la tarea: ")
                response = self.client.update_todo(task_id, title, status, description)
                print(response)
            elif option == "3":
                task_id = input("Ingrese el id de la tarea a eliminar: ")
                response = self.client.delete_todo(task_id)
                print(response)
            elif option == "0":
                break
            else:
                print("Opción no válida")

    def menu(self):
        if self.client.verificarConexion():
            while True:
                self.menuText()
                option = input("Seleccione una opción: ")
                if option == "1":
                    self.login()
                    if self.user:
                        self.menuUser()
                elif option == "2":
                    self.register()
                elif option == "3":
                    self.logout()
                elif option == "0":
                    break
                else:
                    print("Opción no válida")
        else:
            print("No se pudo establecer conexión con el servidor")
    def run(self):
        self.menu()

# Iniciar sesión
"""
login_response = client.login("0000", "1234")
print(login_response)
new_user = {"rut": "1111", "password": "4321"}
register_response = client.register(new_user["rut"], new_user["password"])
print(register_response)
# Obtener todas las tareas del usuario
#todos = client.get_todos()
#print(todos)

# Agregar una nueva tarea
# task = {"title": "Nueva tarea", "description": "Descripción de la nueva tarea"}
# add_response = client.add_todo(task["title"], task["description"])
print(add_response)

# Cerrar sesión
logout_response = client.logout()
print(logout_response)
"""

if __name__ == "__main__":
    menu = menu()
    menu.run()

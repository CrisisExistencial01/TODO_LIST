import requests
import json
class LocalClient:
    def __init__(self):
        self.user = None
        self.url = "http://50.16.235.247:8081"

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

client = LocalClient()

# Ejemplo de uso:
# Iniciar sesión
login_response = client.login("0000", "1234")
print(login_response)
new_user = {"rut": "1111", "password": "4321"}
register_response = client.register(new_user["rut"], new_user["password"])
print(register_response)
# Obtener todas las tareas del usuario
#todos = client.get_todos()
#print(todos)

# Agregar una nueva tarea
task = {"title": "Nueva tarea", "description": "Descripción de la nueva tarea"}
add_response = client.add_todo(task["title"], task["description"])
print(add_response)

# Cerrar sesión
logout_response = client.logout()
print(logout_response)


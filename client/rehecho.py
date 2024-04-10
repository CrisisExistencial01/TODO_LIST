import requests
import json

class LocalClient:
    def __init__(self):
        self.user = None
        self.url = "http://50.16.235.247:8081"

    def verificarConexion(self):
        print("Verificando conexión con el servidor...")
        try:
            response = requests.get(self.url, timeout=3)
            return True
        except requests.exceptions.RequestException:
            return False

    def request(self, method, path, data=None):
        url = self.url + path
        if method == "GET":
            response = requests.get(url)
        elif method == "POST":
            response = requests.post(url, json=data)
        elif method == "PUT":
            response = requests.put(url, json=data)
        elif method == "DELETE":
            response = requests.delete(url)
        return response.json()["msg"]

    def login(self, rut, password):
        self.user = rut
        data = {"user": rut, "password": password}
        return self.request("POST", "/login", data)

    def logout(self):
        self.user = None
        return self.request("GET", "/logout")

    def register(self, rut, password):
        user = {"rut": rut, "password": password}
        return self.request("POST", "/register", user)

    def get_todos(self):
        path = f"/{self.user}/todos"
        return self.request("GET", path)

    def add_todo(self, title, description):
        task = {"user": self.user, "title": title, "description": description}
        path = f"/{self.user}/todos"
        return self.request("POST", path, task)

    def update_todo(self, task_id, title, status, description):
        task = {"title": title, "status": status, "description": description}
        path = f"/{self.user}/todos/{task_id}"
        return self.request("PUT", path, task)

    def delete_todo(self, task_id):
        path = f"/{self.user}/todos/{task_id}"
        return self.request("DELETE", path)

class Menu:
    def __init__(self):
        self.client = LocalClient()
        self.user = None

    # Aquí puedes implementar la lógica del menú de la misma manera que en el código original

if __name__ == "__main__":
    menu = Menu()
    menu.run()

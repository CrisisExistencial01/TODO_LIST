from flask import Flask, request, jsonify
from pymongo import MongoClient

class MongoManager:
    def __init__(self):
        self.client = MongoClient("mongodb://localhost:27017/")
        self.db = self.client["todo"]
        self.users = self.db["users"]
        self.tasks = self.db["tasks"]

    def login(self, rut, password):
        user = self.users.find_one({"rut": rut})
        return user and user["passwd"] == password

    def register(self, data):
        if self.users.find_one({"rut": data["rut"]}):
            return False
        self.users.insert_one(data)
        return True

    def find_user_tasks(self, rut):
        return list(self.tasks.find({"user": rut}))

    def insert_task(self, rut, data):
        data["user"] = rut
        data["id"] = self.tasks.count_documents({"user": rut}) + 1
        data["status"] = "pending"
        self.tasks.insert_one(data)

    def update_task(self, rut, task_id, data):
        query = {"id": task_id, "user": rut}
        if self.tasks.find_one(query):
            self.tasks.update_one(query, {"$set": data})

    def delete_task(self, rut, task_id):
        query = {"id": task_id, "user": rut}
        if self.tasks.find_one(query):
            self.tasks.delete_one(query)

    def delete_user(self, rut):
        self.users.delete_one({"rut": rut})

class RequestManager:
    def __init__(self):
        self.app = Flask(__name__)
        self.mongo = MongoManager()
        self.user_rut = None

    def register_routes(self):
        self.app.route("/logout", methods=["GET"])(self.logout)
        self.app.route("/<user_rut>/todos", methods=["GET"])(self.get_todos)
        self.app.route("/login", methods=["POST"])(self.login)
        self.app.route("/register", methods=["POST"])(self.register)
        self.app.route("/<user_rut>/todos", methods=["POST"])(self.add_todo)
        self.app.route("/<user_rut>/todos/<task_id>", methods=["PUT"])(self.update_todo)
        self.app.route("/<user_rut>/todos/<task_id>", methods=["DELETE"])(self.delete_todo)
        self.app.route("/<user_rut>", methods=["DELETE"])(self.delete_user)

    def login(self):
        data = request.get_json()
        if self.mongo.login(data["user"], data["password"]):
            self.user_rut = data["user"]
            return jsonify({"msg": "Logged in successfully"})
        return jsonify({"msg": "Invalid credentials"})

    def logout(self):
        self.user_rut = None
        return jsonify({"msg": "Logged out successfully"})

    def register(self):
        data = request.get_json()
        if self.mongo.register(data):
            return jsonify({"msg": "Registered successfully"})
        return jsonify({"msg": "User already exists"})

    def get_todos(self, user_rut):
        return jsonify(self.mongo.find_user_tasks(user_rut))

    def add_todo(self, user_rut):
        data = request.get_json()
        self.mongo.insert_task(user_rut, data)
        return jsonify({"msg": "Task added successfully"})

    def update_todo(self, user_rut, task_id):
        data = request.get_json()
        self.mongo.update_task(user_rut, task_id, data)
        return jsonify({"msg": "Task updated successfully"})

    def delete_todo(self, user_rut, task_id):
        self.mongo.delete_task(user_rut, task_id)
        return jsonify({"msg": "Task deleted successfully"})

    def delete_user(self, user_rut):
        self.mongo.delete_user(user_rut)
        return jsonify({"msg": "User deleted successfully"})

    def run(self, host='0.0.0.0', port=8081):
        self.app.run(host=host, port=port, debug=True)

if __name__ == "__main__":
    manager = RequestManager()
    manager.register_routes()
    manager.run()

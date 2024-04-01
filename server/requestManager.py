from flask import Flask, request, jsonify
from mongoManager import MongoManager
class requestManager:

    def __init__(self):
        self.app = Flask(__name__)
        self.mongo = MongoManager()
        self.user_rut = None

    def register_routes(self):

        # associating the routes with the methods of the class

        # GET -> se pueden llamar desde el navegador
        self.app.route("/logout", methods=["GET"])(self.logout)
        self.app.route("/<user_rut>/todos", methods=["GET"])(self.get_todos)

        # POST
        self.app.route("/login", methods=["POST"])(self.login)
        self.app.route("/register", methods=["POST"])(self.register)
        self.app.route("/<user_rut>/todos", methods=["POST"])(self.add_todo)

        # PUT
        self.app.route("/<user_rut>/todos/<task_id>", methods=["PUT"])(self.update_todo)

        # DELETE
        self.app.route("/<user_rut>/todos/<task_id>", methods=["DELETE"])(self.delete_todo)
        self.app.route("/<user_rut>", methods=["DELETE"])(self.delete_user)

    def login(self):
        data = request.get_json()
        user = data["user"]
        password = data["password"]
        if self.mongo.login(user, password):
            self.user_rut = user

            return jsonify({"msg": "Logged in successfully"})
        else:
            return jsonify({"msg": "Invalid credentials"})

    def logout(self):
        self.user_rut = None
        return jsonify({"msg": "Logged out successfully"})

    def register(self):
        data = request.get_json()
        # data = {"user": "user_rut", "password": "password"}
        if self.mongo.register(data): 
            return jsonify({"msg": "Registered successfully"})
        else:
            return jsonify({"msg": "User already exists"})
    
    def get_todos(self):
        todos = self.mongo.find_user_tasks(self.user_rut)
        return jsonify(todos)
    def add_todo(self, user_rut):

        # associating the user rut with the task

        # DATA FORMAT:
        #        tasks collection format:
        #        {
        #            "user": "user's rut",
        #            "title": "Task 1",
        #            "status": "To Do",
        #            "description": "Description of task 1",
        #        }

        data = request.get_json()
        data["user"] = self.user_rut
        self.mongo.insert_task(self.user_rut, data)
        return jsonify({"msg": "Task added successfully"})

    def update_todo(self, user_rut, task_id):
        data = request.get_json()
        data["user"] = self.user_rut
        self.mongo.update_task(self.user_rut, task_id, data)
        return jsonify({"msg": "Task updated successfully"})

    def delete_todo(self, user_rut, task_id):
        self.mongo.delete_task(self.user_rut, task_id)

        return jsonify({"msg": "Task deleted successfully"})

    def delete_user(self, user_rut):
        self.mongo.delete_user(self.user_rut)
        return jsonify({"msg": "User deleted successfully"})

    def run(self, host ='0.0.0.0',port=8081):
        self.app.run(host=host,port=port, debug=True)

if __name__ == "__main__":
    manager = requestManager()
    manager.register_routes()
    manager.run()

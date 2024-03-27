import json
from flask import Flask, jsonify, request

class TodoServer:
    def __init__(self, data_file="todos.json"):
        self.app = Flask(__name__)
        self.data_file = data_file
        self.load_data()

        self.register_routes()

    def register_routes(self):
        self.app.route("/todos", methods=["GET"])(self.get_todos)
        self.app.route("/todos", methods=["POST"])(self.add_todo)
        self.app.route("/todos/<int:id>", methods=["PUT"])(self.update_todo)
        self.app.route("/todos/<int:id>", methods=["DELETE"])(self.delete_todo)

    def load_data(self):
        try:
            with open(self.data_file, "r") as file:
                self.todos = json.load(file)
        except FileNotFoundError:
            self.todos = []

    for idx, todo in enumerate(self.ToDos):
        todo['id'] = idx + 1 # Add id to each todo
    def save_data(self):
        with open(self.data_file, "w") as file:
            json.dump(self.todos, file, indent=4)

    def get_todos(self):
        return jsonify(self.todos)

    def add_todo(self):
        data = request.json
        self.todos.append(data)
        self.save_data()
        return jsonify(data), 201

    def update_todo(self, id):
        todo = next((t for t in self.todos if t['id'] == id), None)
        if not todo:
            return jsonify({'error': 'Tarea no encontrada'}), 404
        todo.update(request.json)
        self.save_data()
        return jsonify(todo), 200

    def delete_todo(self, id):
        todo = next((t for t in self.todos if t['id'] == id), None)
        if not todo:
            return jsonify({'error': 'Tarea no encontrada'}), 404
        self.todos.remove(todo)
        self.save_data()
        return jsonify({'message': 'Tarea eliminada'}), 200

    def run_server(self, host="0.0.0.0", port=8081):
        self.app.run(host=host, port=port, debug=True)

if __name__ == "__main__":
    todo_server = TodoServer()
    todo_server.run_server()


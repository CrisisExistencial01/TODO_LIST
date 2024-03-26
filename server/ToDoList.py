from flask import Flask, jsonify, request
"""

SERVIDOR TODO LIST FLASK

"""
todos = [] # LISTADO DE TAREAS
def create_app():
    app = Flask(__name__)
    return app
app = create_app()

@app.route("todos")

def get_todos():

    return jsonify(todos) # RETORNA TODOS LOS TODOS EN FORMATO JSON

@app.route("todos", methods=["POST"])

def add_todos():
    dataRequest = request.json() # OBTIENE LOS DATOS DE LA PETICION EN FORMATO JSON
    todos.append(dataRequest) # AGREGA LA TAREA A LA LISTA DE TAREAS
    return jsonify(dataRequest), 201 # RETORNA LA TAREA AGREGADA EN FORMATO JSON

@app.route("todos/<int:id>", methods=["PUT"])
   
def update_todos(id):
    todo = next((t for t in todos if t['id'] == todo_id), None) # BUSCA LA TAREA POR EL ID
    if not todo:
        return jsonify({'error': 'Tarea no encontrada'}), 404 # RETORNA UN ERROR SI NO SE ENCUENTRA LA TAREA
    todo.update(request.json) # ACTUALIZA LA TAREA
        return jsonify(todo), 200 # RETORNA LA TAREA ACTUALIZADA EN FORMATO JSON

@app.route("todos/<int:id>", methods=["DELETE"])

def delete_todos(id):
    todo = next((t for t in todos if t['id'] == todo_id), None) # BUSCA LA TAREA POR EL ID
    if not todo:
        return jsonify({'error': 'Tarea no encontrada'}), 404
    todos.remove(todo) # ELIMINA LA TAREA
    return jsonify({'message': 'Tarea eliminada'}), 200 # RETORNA UN MENSAJE DE TAREA ELIMINADA
# con eso ya se elimina la tarea o hay que actualizarla?

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8081, debug=True)
    print("ToDo List: ")
    print(get_todos())
    # Agregar una nueva tarea
    new_todo = {'id': 1, 'task': 'Completar proyecto'}
    add_todo(new_todo)

    # Actualizar una tarea existente
    updated_todo = {'task': 'Completar proyecto de todos los requisitos'}
    update_todo(1, updated_todo)

    # Eliminar una tarea
    delete_todo(1)

    # Obtener todas las tareas nuevamente
    print('Lista de tareas actualizada:')
    print(get_todos())

~
~


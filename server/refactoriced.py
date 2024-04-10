rom flask import Flask, request, jsonify
from pymongo import MongoClient

app = Flask(__name__)
client = MongoClient('localhost', 27017)  # Conecta a MongoDB localmente
db = client['mydatabase']  # Nombre de la base de datos
tasks_collection = db['tasks']  # Colección para almacenar las tareas

@app.route('/VH_create_user', methods=['POST'])
def VH_create_user():
    data = request.json
    user_id = data.get('VH_user_id')
    if user_id:
        tasks_collection.insert_one({'user_id': user_id, 'tasks': []})
        return jsonify({'message': 'Usuario creado exitosamente', 'user_id': user_id}), 201
    else:
        return jsonify({'error': 'No se proporcionó un ID de usuario'}), 400

@app.route('/VH_create_task/<user_id>', methods=['POST'])
def VH_create_task(user_id):
    data = request.json
    title = data.get('VH_title')
    description = data.get('VH_description')
    if title and description:
        tasks_collection.update_one({'user_id': user_id}, {'$push': {'tasks': {'title': title, 'description': description}}})
        return jsonify({'message': 'Tarea creada exitosamente'}), 201
    else:
        return jsonify({'error': 'Falta el título o la descripción de la tarea'}), 400

@app.route('/VH_list_tasks/<user_id>', methods=['GET'])
def VH_list_tasks(user_id):
    user_tasks = tasks_collection.find_one({'user_id': user_id}, {'_id': 0, 'tasks': 1})
    if user_tasks:
        return jsonify(user_tasks['tasks']), 200
    else:
        return jsonify({'message': 'Usuario no encontrado'}), 404

@app.route('/VH_update_task/<user_id>/<int:task_index>', methods=['PUT'])
def VH_update_task(user_id, task_index):
    data = request.json
    title = data.get('VH_title')
    description = data.get('VH_description')
    if title and description:
        tasks_collection.update_one({'user_id': user_id}, {'$set': {'tasks.' + str(task_index): {'title': title, 'description': description}}})
        return jsonify({'message': 'Tarea modificada exitosamente'}), 200
    else:
        return jsonify({'error': 'Falta el título o la descripción de la tarea'}), 400

@app.route('/VH_delete_task/<user_id>/<int:task_index>', methods=['DELETE'])
def VH_delete_task(user_id, task_index):
    result = tasks_collection.update_one({'user_id': user_id}, {'$unset': {'tasks.' + str(task_index): 1}})
    if result.modified_count:
        return jsonify({'message': 'Tarea eliminada exitosamente'}), 200
    else:
        return jsonify({'error': 'Usuario o tarea no encontrada'}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8081)


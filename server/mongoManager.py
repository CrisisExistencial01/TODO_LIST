from pymongo import MongoClient
# MongoManager class is a class that is used to manage the connection to the MongoDB database.
# DATA FORMAT:
#        users collection format:
#        {
#            "username": "John",
#            "password": "1234",
#        }
#
#        tasks collection format:
#        {
#            "title": "Task 1",
#            "status": "To Do",
#            "description": "Description of task 1",
#        }
class MongoManager:
    def __init__(self):
        self.client = MongoClient("mongodb://localhost:27017/")
        # Database
        self.db = self.client["todo"]
        # Collections in the database
        self.users = self.get_collection("users")
        self.tasks = self.get_collection("tasks")


    # Generic functions that abstract mongoDB functions
    def insert(self, collection, data):
        self.collection.insert_one(data)

    def find(self, query):
        return self.collection.find(query)

    def update(self, query, data):
        self.collection.update_one(query, data)

    def delete(self, query):
        self.collection.delete_one(query)
    
    def get_collection(self, collection_name):
        return self.db[collection_name]
    # User functions
    def insert_user(self, data):
        self.db.insert(self.db["users"], data)
    def update_user(self, query, data):
        self.db.update(self.db["users"], query, data)
    # search by rut
    def find_user(self, query):
        return self.db.find(self.db.users, {"rut": query})
    def delete_user(self, query):
        self.db.delete(self.db.users, query)

    # Task functions
    def insert_task(self, data):
        self.db.insert(self.db["tasks"], data)
    def find_task(self, query): # query is a dictionary with the query to be executed in the database (e.g. {"name": "John"})
        return self.db.find(self.db["tasks"], query)
    def update_task(self, query, data):
        self.db.update(self.db["tasks"], query, data)
    def delete_task(self, query):
        self.db.delete(self.db.tasks, query)
mongo = MongoClient()
user = {"rut": "0000", "passwd": "1234"}
mongo.insert_user(user)
resultado = mongo.find_user("PEPE")
for doc in resultado:
    print(resultado)

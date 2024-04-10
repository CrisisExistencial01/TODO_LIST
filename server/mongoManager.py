from pymongo import MongoClient
# MongoManager class is a class that is used to manage the connection to the MongoDB database.
# DATA FORMAT:
#        users collection format:
#        {
#            "rut": "user's rut",
#            "passwd": "user's password",
#        }
#
#        tasks collection format:
#        {
#            "user": "user's rut",
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
        try:
            collection.insert_one(data)
        except PyMongoError as e:
            print("Error inserting data: ", e)

    def find(self, collection, query):
        try:
            return collection.find(query)
        except PyMongoError as e:
            print("Error finding data: ", e)

    def update(self, collection, query, data):
        try:
            collection.update_one(query, {"$set": data})
        except PyMongoError as e:
            print("Error updating data: ", e)

    def delete(self, collection, query):
        try:
            collection.delete_one(query)
        except PyMongoError as e:
            print("Error deleting data: ", e)

   # Specific functions for the collections in the database
    def get_collection(self, collection_name):
        return self.db[collection_name]

    def get_tasks_length(self, rut):
        return self.tasks.count_documents({"user": rut})

    # User functions
    def login(self, rut, passwd):
        user = self.find_user(rut)
        for doc in user:
            if doc["passwd"] == passwd:
                return True
        return False

    def register(self, data):
        if self.find_user(data["rut"]):
            print("User already exists")
        else:
            self.insert_user(data)

    def update_user(self, query, data):
        if self.find_user(query["rut"]):
            self.update(self.users, query, data)
        else:
            print("User doesn't exist")

    def find_user(self, rut):
        return self.find(self.users, {"rut": rut})

    def delete_user(self, rut):
        self.delete(self.users, {"rut": rut})

    # Task functions
    def insert_task(self, rut, data): # query is a dictionary
# FORMAT:
#   rut = query["user"]
#   title = query["title"]
#   desc = query["description"]
#   status = query["status"]

        data["user"] = rut
        # add an id to the task
        data["id"] = self.get_tasks_length(rut) + 1
        
        # default status is pending
        data["status"] = "pending"

        self.insert(self.tasks, data)

    def find_user_tasks(self, rut): 
        return self.find(self.tasks, {"user": rut}) # returns a dictionary with the tasks of the user

    def find_task(self, rut, query):
        return self.find(self.tasks, query) # returns a dictionary with the task

    def update_task(self, rut, task_id, data):
        query = {"id": task_id}
        query["user"] = rut
        self.update(self.tasks, query, data)

    def delete_task(self, rut, query):
        query["user"] = rut
        self.delete(self.tasks, query)

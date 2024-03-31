from mongoDB import MongoManager

class Tester:
    def __init__(self):
        self.mongo = MongoManager()
        self.test()
    def test(self):
        # Inserting users and tasks
        self.mongo.insert_task({"title": "Task 1", "status": "To Do", "description": "Description of task 1"})
        self.mongo.insert_user({"username": "John", "password": "1234"})
        # Finding users and tasks
        print(self.mongo.find_user({"username": "John"}))
        print(self.mongo.find_task({"title": "Task 1"}))
        # Updating users and tasks
        self.mongo.update_user({"username": "John"}, {"password": "5678"})
        self.mongo.update_task({"title": "Task 1"}, {"status": "Done"})
        # Deleting users and tasks
        self.mongo.delete_user({"username": "John"})
        self.mongo.delete_task({"title": "Task 1"})

tester = Tester()

tester.test()

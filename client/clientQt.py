import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
import requests

class TodoApp(QWidget):
    def __init__(self):
        super().__init__()
        self.drawLogin()
        self.url = 'http://50.16.235.247:8081' # Server_ip:PORT

    def drawLogin(self):

        self.setWindowTitle('Todo App')
        self.layout = QVBoxLayout()

        self.label_rut = QLabel('RUT:')
        self.input_rut = QLineEdit()
        self.layout.addWidget(self.label_rut)
        self.layout.addWidget(self.input_rut)

        self.label_password = QLabel('Password:')
        self.input_password = QLineEdit()
        self.input_password.setEchoMode(QLineEdit.Password)
        self.layout.addWidget(self.label_password)
        self.layout.addWidget(self.input_password)

        self.button_login = QPushButton('Login')
        self.button_login.clicked.connect(self.login)
        self.layout.addWidget(self.button_login)

        self.label_message = QLabel('')
        self.layout.addWidget(self.label_message)

        self.button_register = QPushButton('Register')
        self.button_register.clicked.connect(self.register)
        self.layout.addWidget(self.button_register)

        self.setLayout(self.layout)


    def login(self):
        rut = self.input_rut.text()
        password = self.input_password.text()
        response = requests.post(f'{self.url}/login', json={'user': rut, 'password': password})
        if response.status_code == 200:
            message = response.json()['msg']
            self.label_message.setText(message)
        else:
            error_message = response.json().get('msg', 'An error occurred')
            QMessageBox.critical(self, 'Error', error_message)

    def register(self):
        rut = self.input_rut.text()
        password = self.input_password.text()
        response = requests.post(f'{self.url}/register', json={'rut': rut, 'password': password})
        if response.status_code == 200:
            message = response.json()['msg']
            self.label_message.setText(message)
        else:
            error_message = response.json().get('msg', 'An error occurred')
            QMessageBox.critical(self, 'Error', error_message)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    todo_app = TodoApp()
    todo_app.show()
    sys.exit(app.exec_())


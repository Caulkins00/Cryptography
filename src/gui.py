import sys
from PyQt6.QtWidgets import (QApplication,
    QWidget,
    QPushButton,
    QLabel,
    QLineEdit,
    QGridLayout,
    QMessageBox,
    QStackedLayout,
    QVBoxLayout)

from PyQt6.QtCore import Qt
from userLogin import *

class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Login Form')
        self.resize(800, 400)

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.stackedLayout = QStackedLayout()

        self.loginPage = QWidget()
        self.loginPageLayout = QGridLayout()

        label_name = QLabel('<font size="4"> Username </font>')
        self.lineEdit_username = QLineEdit()
        self.lineEdit_username.setPlaceholderText('Please enter your username')
        self.lineEdit_username.setStyleSheet("background-color: rgb(136, 145, 158);")
        self.loginPageLayout.addWidget(label_name, 0, 0)
        self.loginPageLayout.addWidget(self.lineEdit_username, 0, 1)

        label_password = QLabel('<font size="4"> Password </font>')
        self.lineEdit_password = QLineEdit()
        self.lineEdit_password.setPlaceholderText('Please enter your password')
        self.lineEdit_password.setStyleSheet("background-color: rgb(136, 145, 158);")
        self.loginPageLayout.addWidget(label_password, 1, 0)
        self.loginPageLayout.addWidget(self.lineEdit_password, 1, 1)

        button_login = QPushButton('Login')
        button_login.clicked.connect(self.check_password)
        button_login.setStyleSheet("background-color: rgb(136, 145, 158);")
        self.loginPageLayout.addWidget(button_login, 2, 0, 1, 2)
        self.loginPageLayout.setRowMinimumHeight(2, 75)

        self.label_message = QLabel('<font size="4"> Welcome! </font>',self)
        self.label_message.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.loginPageLayout.addWidget(self.label_message, 3, 0, 1, 2)

        add_button = QPushButton('New here? Create an account!')
        add_button.clicked.connect(self.add_user)
        add_button.setStyleSheet("background-color: rgb(136, 145, 158);")
        self.loginPageLayout.addWidget(add_button, 4, 0, 1, 2)

        self.loginPage.setLayout(self.loginPageLayout)
        self.stackedLayout.addWidget(self.loginPage)

        self.tablePage = QWidget()
        self.tablePageLayout = QVBoxLayout()
        self.label = QLabel('Congrats!')
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # self.tablePage.setAttribute(Qt.WA_StyledBackground, True)
        # self.tablePage.setStyleSheet('background-color: red;')
        self.tablePageLayout.addWidget(self.label)

        self.addPage = QWidget()
        self.addPageLayout = QGridLayout()

        add_name = QLabel('<font size="4"> Username </font>')
        self.lineEditAdd_username = QLineEdit()
        self.lineEditAdd_username.setPlaceholderText('Please enter your username')
        self.lineEditAdd_username.setStyleSheet("background-color: rgb(136, 145, 158);")
        self.addPageLayout.addWidget(add_name, 1, 0)
        self.addPageLayout.addWidget(self.lineEditAdd_username, 0, 1)

        add_password = QLabel('<font size="4"> Password </font>')
        self.lineEditAdd_password = QLineEdit()
        self.lineEditAdd_password.setPlaceholderText('Please enter your password')
        self.lineEditAdd_password.setStyleSheet("background-color: rgb(136, 145, 158);")
        self.addPageLayout.addWidget(add_password, 1, 0)
        self.addPageLayout.addWidget(self.lineEditAdd_password, 1, 1)

        button_add = QPushButton('Add User')
        # button_add.clicked.connect(add_user_gui())
        button_add.setStyleSheet("background-color: rgb(136, 145, 158);")
        self.addPageLayout.addWidget(button_add, 2, 0, 1, 2)
        self.addPageLayout.setRowMinimumHeight(2, 75)


        self.setStyleSheet("background-color: rgb(106,137,189);")

        self.tablePage.setLayout(self.tablePageLayout)
        self.addPage.setLayout(self.addPageLayout)
        self.stackedLayout.addWidget(self.tablePage)
        self.stackedLayout.addWidget(self.addPage)

        layout.addLayout(self.stackedLayout)

    def check_password(self):
        msg = QMessageBox()
        if is_valid_credentials(self.lineEdit_username.text(), self.lineEdit_password.text().encode()):
            # msg.setText('Success')
            # msg.exec()
            self.stackedLayout.setCurrentIndex(1)
            self.populate_table(self.lineEdit_password.text().encode())
        else:
            # msg.setText('Incorrect Password')
            self.label_message.setText('<font size="4"> Incorrect username or password. Please try again. </font>')
            # msg.exec()

    def add_user(self):
         self.stackedLayout.setCurrentIndex(2)

    def populate_table(master_password, self):
         pass

if __name__ == '__main__':
	app = QApplication(sys.argv)

	window = Window()
	window.show()

	sys.exit(app.exec())
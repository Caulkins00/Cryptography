import sys, random, string
from PyQt6.QtWidgets import (QApplication,
    QWidget,
    QPushButton,
    QLabel,
    QLineEdit,
    QGridLayout,
    QMessageBox,
    QStackedLayout,
    QVBoxLayout,
    QHBoxLayout,
    QTableWidget,
    QTableWidgetItem,
    QTableView
    )

from PyQt6.QtCore import Qt, QAbstractListModel
import userLogin
# from userLogin import *

username = None

class TableModel(QAbstractListModel):
    def __init__(self, data):
        super(TableModel, self).__init__()
        self._passwords = data

    def data(self, index, role):
        if role == Qt.ItemDataRole.DisplayRole:
            return self._passwords[index.row()][index.column()]

    def rowCount(self, index):
        return len(self._passwords)
    
    def columnCount(self, index):
        return len(self._passwords[0])

class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Password Manager')
        self.resize(800, 400)

        self.username = None

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.stackedLayout = QStackedLayout()

        # ---------- Login ----------

        self.loginPage = QWidget()
        self.loginPageLayout = QGridLayout()

        label_name = QLabel('<font size="4"> Username </font>')
        self.lineEdit_username = QLineEdit()
        self.lineEdit_username.setPlaceholderText('Please enter your username')
        # self.lineEdit_username.setStyleSheet("background-color: rgb(136, 145, 158);")
        self.loginPageLayout.addWidget(label_name, 0, 0)
        self.loginPageLayout.addWidget(self.lineEdit_username, 0, 1)

        label_password = QLabel('<font size="4"> Password </font>')
        self.lineEdit_password = QLineEdit()
        self.lineEdit_password.setEchoMode(QLineEdit.EchoMode.Password)
        self.lineEdit_password.setPlaceholderText('Please enter your password')
        # self.lineEdit_password.setStyleSheet("background-color: rgb(136, 145, 158);")
        self.loginPageLayout.addWidget(label_password, 1, 0)
        self.loginPageLayout.addWidget(self.lineEdit_password, 1, 1)

        button_login = QPushButton('Login')
        button_login.clicked.connect(self.check_password)
        # button_login.setStyleSheet("background-color: rgb(136, 145, 158);")
        button_login.resize(150,50)
        self.loginPageLayout.addWidget(button_login, 2, 0, 1, 2)
        # self.loginPageLayout.setRowMinimumHeight(2, 75)

        self.label_message = QLabel('<font size="4"> Welcome! </font>',self)
        self.label_message.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.loginPageLayout.addWidget(self.label_message, 3, 0, 1, 2)

        add_button = QPushButton('New here? Create an account!')
        add_button.clicked.connect(self.switch_add)
        # add_button.setStyleSheet("background-color: rgb(136, 145, 158);")
        self.loginPageLayout.addWidget(add_button, 4, 0, 1, 2)

        self.loginPage.setLayout(self.loginPageLayout)
        self.stackedLayout.addWidget(self.loginPage)

        # ---------- Table ----------

        buttonAdd_password = QPushButton('Add Password')
        buttonAdd_password.clicked.connect(self.page_add_password)
        self.query = QLineEdit()
        self.query.setPlaceholderText("Search...")
        self.query.textChanged.connect(self.search)

        self.table = QTableView()

        data = userLogin.pull_table(username)

        self.model = TableModel(data)
        self.table.setModel(self.model)
        
        # self.table.setHorizontalHeaderLabels(["username", "password"])

        self.tablePage = QWidget()
        self.tablePageLayout = QVBoxLayout()

        self.tablePageLayout.addWidget(buttonAdd_password)
        self.tablePageLayout.addWidget(self.query)
        self.tablePageLayout.addWidget(self.table)

        self.tablePage.setLayout(self.tablePageLayout)
        self.stackedLayout.addWidget(self.tablePage)

        # ---------- Add User ----------

        self.addPage = QWidget()
        self.addPageLayout = QGridLayout()

        button_back = QPushButton('Back')
        button_back.clicked.connect(self.page_back)
        # button_back.setStyleSheet("background-color: rgb(136, 145, 158);")
        self.addPageLayout.addWidget(button_back, 0, 0, )

        add_name = QLabel('<font size="4"> Username </font>')
        self.lineEditAdd_username = QLineEdit()
        self.lineEditAdd_username.setPlaceholderText('Please enter your username')
        # self.lineEditAdd_username.setStyleSheet("background-color: rgb(136, 145, 158);")
        self.addPageLayout.addWidget(add_name, 1, 0)
        self.addPageLayout.addWidget(self.lineEditAdd_username, 1, 1)

        add_password = QLabel('<font size="4"> Password </font>')
        self.lineEditAdd_password = QLineEdit()
        self.lineEditAdd_password.setEchoMode(QLineEdit.EchoMode.Password)
        self.lineEditAdd_password.setPlaceholderText('Please enter your password')
        # self.lineEditAdd_password.setStyleSheet("background-color: rgb(136, 145, 158);")
        self.addPageLayout.addWidget(add_password, 2, 0)
        self.addPageLayout.addWidget(self.lineEditAdd_password, 2, 1)

        button_add = QPushButton('Add User')
        button_add.clicked.connect(self.add_user)
        # button_add.setStyleSheet("background-color: rgb(136, 145, 158);")
        self.addPageLayout.addWidget(button_add, 3, 0, 1, 2)
        self.addPageLayout.setRowMinimumHeight(2, 75)

        self.addPage.setLayout(self.addPageLayout)
        self.stackedLayout.addWidget(self.addPage)

        # ---------- Add Password ----------

        self.newPage = QWidget()
        self.newPageLayout = QGridLayout()

        button_back2 = QPushButton('Back')
        button_back2.clicked.connect(self.page_back)
        # button_back.setStyleSheet("background-color: rgb(136, 145, 158);")
        self.newPageLayout.addWidget(button_back2, 0, 0, )

        new_username = QLabel('<font size="4"> Username </font>')
        self.lineEditNew_username = QLineEdit()
        self.lineEditNew_username.setPlaceholderText('Please enter your username')
        # self.lineEditAdd_username.setStyleSheet("background-color: rgb(136, 145, 158);")
        self.newPageLayout.addWidget(new_username, 1, 0)
        self.newPageLayout.addWidget(self.lineEditNew_username, 1, 1)

        new_password = QLabel('<font size="4"> Password </font>')
        self.lineEditNew_password = QLineEdit()
        self.lineEditNew_password.setEchoMode(QLineEdit.EchoMode.Password)
        self.lineEditNew_password.setPlaceholderText('Please enter your password')
        # self.lineEditAdd_password.setStyleSheet("background-color: rgb(136, 145, 158);")
        self.newPageLayout.addWidget(new_password, 2, 0)
        self.newPageLayout.addWidget(self.lineEditNew_password, 2, 1)

        button_add2 = QPushButton('Add Password')
        button_add2.clicked.connect(self.add_password)
        # button_add.setStyleSheet("background-color: rgb(136, 145, 158);")
        self.newPageLayout.addWidget(button_add2, 3, 0, 1, 2)
        self.newPageLayout.setRowMinimumHeight(2, 75)

        self.label_message_new = QLabel('<font size="4"> Hi! </font>',self)
        self.label_message_new.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.newPageLayout.addWidget(self.label_message_new, 4, 0, 1, 2)

        # self.setStyleSheet("background-color: rgb(106,137,189);")

        self.newPage.setLayout(self.newPageLayout)
        self.stackedLayout.addWidget(self.newPage)

        layout.addLayout(self.stackedLayout)

    def check_password(self):
        msg = QMessageBox()
        if userLogin.is_valid_credentials(self.lineEdit_username.text(), self.lineEdit_password.text().encode()):
            # msg.setText('Success')
            # msg.exec()
            self.stackedLayout.setCurrentIndex(1)
            self.username = self.lineEdit_username.text()
            username = self.lineEdit_username.text()
            # print(self.username)
            self.populate_table()
        else:
            # msg.setText('Incorrect Password')
            self.label_message.setText('<font size="4"> Incorrect username or password. Please try again. </font>')
            # msg.exec()

    def switch_add(self):
        self.stackedLayout.setCurrentIndex(2)

    def add_user(self):
        if userLogin.add_user_gui(self.lineEditAdd_username.text(), self.lineEditAdd_password.text().encode()):
            self.stackedLayout.setCurrentIndex(1)
            username = self.lineEditAdd_username.text()
            userLogin.create_table(username)
        else:
            self.label_message_add.setText('<font size="3"> This username is already taken by another user. Please pick a new one. </font>')

    def page_back(self):
        self.stackedLayout.setCurrentIndex(0)

    def page_add_password(self):
        self.stackedLayout.setCurrentIndex(3)

    def search(self, s):
        # clear current selection.
        self.table.setCurrentItem(None)

        if not s:
            # Empty string, don't search.
            return

        matching_items = self.table.findItems(s, Qt.MatchFlag.MatchContains)
        if matching_items:
            # we have found something
            item = matching_items[0]  # take the first
            self.table.setCurrentItem(item)

    # def set_username(self):
    #     username = self.lineEdit_username.text()
    #     print(username)

    def add_password(self):
        # print(self.username)
        userLogin.add_password(self.username, self.lineEditNew_username.text(), self.lineEditNew_password.text())
        self.model.layoutChanged.emit()
        # self.populate_table
        self.stackedLayout.setCurrentIndex(1)

    def populate_table(self):
        data = userLogin.pull_table(self.username)
        self.model._passwords = data
        self.model.layoutChanged.emit()

        # if not len(data)==0:
        #     # self.tablePageLayout.removeWidget(self.table)

        #     self.table.setRowCount(len(data))
        #     self.table.setColumnCount(len(data[0]))

        #     for c in range(len(data)):
        #         for r in range(len(data[0])):
        #             x = QTableWidgetItem(data[c][r])
        #             self.table.setItem(c, r, x)

            # self.tablePageLayout.addWidget(self.table)

if __name__ == '__main__':
	app = QApplication(sys.argv)

	window = Window()
	window.show()

	sys.exit(app.exec())
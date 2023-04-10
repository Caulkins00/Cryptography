# import sys
# from PyQt6 import QtCore, QtGui, QtWidgets
# from PyQt6.QtCore import Qt


# class TableModel(QtCore.QAbstractTableModel):
#     def __init__(self, data):
#         super(TableModel, self).__init__()
#         self._data = data

#     def data(self, index, role):
#         if role == Qt.ItemDataRole.DisplayRole:
#             # See below for the nested-list data structure.
#             # .row() indexes into the outer list,
#             # .column() indexes into the sub-list
#             return self._data[index.row()][index.column()]

#     def rowCount(self, index):
#         # The length of the outer list.
#         return len(self._data)

#     def columnCount(self, index):
#         # The following takes the first sub-list, and returns
#         # the length (only works if all rows are an equal length)
#         return len(self._data[0])


# class MainWindow(QtWidgets.QMainWindow):
#     def __init__(self):
#         super().__init__()

#         self.table = QtWidgets.QTableView()

#         data = [
#           [4, 9, 2],
#           [1, 0, 0],
#           [3, 5, 0],
#           [3, 3, 2],
#           [7, 8, 9],
#         ]

#         self.model = TableModel(data)
#         self.table.setModel(self.model)

#         self.setCentralWidget(self.table)


# app=QtWidgets.QApplication(sys.argv)
# window=MainWindow()
# window.show()
# app.exec()

# ________

# from PyQt6 import QtCore, QtGui


# class MainWindow(QtGui.QMainWindow):
#     def __init__(self, parent=None):
#         super(MainWindow, self).__init__(parent)
#         self.central_widget = QtGui.QStackedWidget()
#         self.setCentralWidget(self.central_widget)
#         login_widget = LoginWidget(self)
#         login_widget.button.clicked.connect(self.login)
#         self.central_widget.addWidget(login_widget)
#     def login(self):
#         logged_in_widget = LoggedWidget(self)
#         self.central_widget.addWidget(logged_in_widget)
#         self.central_widget.setCurrentWidget(logged_in_widget)


# class LoginWidget(QtGui.QWidget):
#     def __init__(self, parent=None):
#         super(LoginWidget, self).__init__(parent)
#         layout = QtGui.QHBoxLayout()
#         self.button = QtGui.QPushButton('Login')
#         layout.addWidget(self.button)
#         self.setLayout(layout)
#         # you might want to do self.button.click.connect(self.parent().login) here


# class LoggedWidget(QtGui.QWidget):
#     def __init__(self, parent=None):
#         super(LoggedWidget, self).__init__(parent)
#         layout = QtGui.QHBoxLayout()
#         self.label = QtGui.QLabel('logged in!')
#         layout.addWidget(self.label)
#         self.setLayout(layout)



# if __name__ == '__main__':
#     app = QtGui.QApplication([])
#     window = MainWindow()
#     window.show()
#     app.exec_()

import sys

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QStackedLayout,
    QVBoxLayout,
    QWidget,
)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("My App")

        pagelayout = QVBoxLayout()
        button_layout = QHBoxLayout()
        self.stacklayout = QStackedLayout()

        pagelayout.addLayout(button_layout)
        pagelayout.addLayout(self.stacklayout)

        btn = QPushButton("red")
        btn.pressed.connect(self.activate_tab_1)
        button_layout.addWidget(btn)
        self.stacklayout.addWidget(self.Color("red"))

        btn = QPushButton("green")
        btn.pressed.connect(self.activate_tab_2)
        button_layout.addWidget(btn)
        self.stacklayout.addWidget(self.Color("green"))

        btn = QPushButton("yellow")
        btn.pressed.connect(self.activate_tab_3)
        button_layout.addWidget(btn)
        self.stacklayout.addWidget(self.Color("yellow"))

        widget = QWidget()
        widget.setLayout(pagelayout)
        self.setCentralWidget(widget)

    def activate_tab_1(self):
        self.stacklayout.setCurrentIndex(0)

    def activate_tab_2(self):
        self.stacklayout.setCurrentIndex(1)

    def activate_tab_3(self):
        self.stacklayout.setCurrentIndex(2)
    
    def Color(self, color):
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(palette.ColorRole.Window, color(color))
        self.setPalette(palette)


app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()
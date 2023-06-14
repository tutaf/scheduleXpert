from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import Qt
import sys
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton

from entities import Teacher


class Ui2(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui2, self).__init__()
        uic.loadUi('groups_cabinets.ui', self)

        self.button_teachers = self.findChild(QtWidgets.QToolButton, 'navigation_buttonAvailability')
        # self.button_teachers.clicked.connect(self.buttonTeachersClicked)
        self.button_generate = self.findChild(QtWidgets.QToolButton, 'navigation_buttonGenerateTimetable')
        # self.button_generate.clicked.connect(self.buttonGenerateClicked)

        self.show()
    def AddGroupButton(self):
        class Group



cabinets = {}
groups = {}

app = QtWidgets.QApplication(sys.argv)
window2 = Ui2()
app.exec_()

from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import Qt
import sys
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QTableWidget, QHeaderView, QCheckBox
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QInputDialog


from entities import Teacher, Group, Room
from scheduling_algorithms import GeneticAlgorithm


class Ui1(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui1, self).__init__()
        uic.loadUi('teacher_abailability.ui', self)

        self.button_groups = self.findChild(QtWidgets.QToolButton, 'navigation_buttonGroupsAndRooms')
        self.button_groups.clicked.connect(self.buttonGroupsClicked)
        self.button_generate = self.findChild(QtWidgets.QToolButton, 'navigation_buttonGenerateTimetable')
        self.button_generate.clicked.connect(self.buttonGenerateClicked)
        self.button_add_teacher = self.findChild(QtWidgets.QPushButton, 'teachers_buttonAddTeacher')
        self.button_add_teacher.clicked.connect(self.buttonAddTeacherClicked)
        self.list_widget_teachers = self.findChild(QtWidgets.QListWidget, 'teachers_listWidget')
        self.list_widget_teachers.currentRowChanged.connect(self.list_widget_selection_changed)
        self.label_table_title = self.findChild(QtWidgets.QLabel, "table_labelTableTitle")
        self.label_teacher_quantity = self.findChild(QtWidgets.QLabel, "teachers_labelTeacherQuantity")
        self.button_add_subject = self.findChild(QtWidgets.QPushButton, 'subjects_buttonAdd')
        self.button_add_subject.clicked.connect(self.buttonAddSubjectClicked)
        self.label_subject_list = self.findChild(QtWidgets.QLabel, 'subjects_labelSubjectList')
        self.table_widget = self.findChild(QtWidgets.QTableWidget, "table_tableWidget")

        self.table_widget.setRowCount(5)
        self.table_widget.setColumnCount(5)

        self.table_widget.setHorizontalHeaderLabels(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'])
        self.table_widget.setVerticalHeaderLabels(
            ['8.00-9.30', '9.45-11.15', '11.30-13.00', '13.30-15.00', '15.15-16.45'])

        header = self.table_widget.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeToContents)
        vheader = self.table_widget.verticalHeader()
        vheader.setSectionResizeMode(QHeaderView.ResizeToContents)

        self.table_widget.cellClicked.connect(self.table_cell_clicked)  # Connect cellClicked signal
        self.table_widget.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)

        self.table_widget.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.table_widget.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)

        for i in range(5):
            for j in range(5):
                check_box = QCheckBox()
                check_box.setText('')
                check_box.setCheckState(Qt.Unchecked)
                check_box.stateChanged.connect(self.check_state_changed)

                # Center align the checkbox
                check_box.setStyleSheet("QCheckBox {margin-left: 80%;}")

                self.table_widget.setCellWidget(i, j, check_box)

        # set stylesheet
        self.table_widget.setStyleSheet('''
                    QTableWidget {
                        gridline-color: #000;
                        font-size: 15px;
                    }
                    QHeaderView::section {
                        background-color: #f0f0f0;
                        padding: 5px;
                        border: 1px solid #ddd;
                        font-size: 18px;
                    }
                    QCheckBox {
                        margin-left:50%; margin-right:50%;
                    }
                ''')

        self.show()

    def buttonGroupsClicked(self):
        window2.show()
        window1.hide()

    def buttonGenerateClicked(self):
        window3.show()
        window1.hide()

    def list_widget_selection_changed(self, current_row):
        selected_text = self.list_widget_teachers.item(current_row).text()
        self.label_table_title.setText(f"## {selected_text}")

        # Load teacher's availability data into UI
        current_teacher_index = self.getCurrentTeacherIndex()
        if current_teacher_index is not None:
            current_teacher = teachers[current_teacher_index]
            for i in range(5):
                for j in range(5):
                    checkbox = self.table_widget.cellWidget(i, j)
                    checkbox.setChecked(current_teacher.availability[i][j])

            # Update the subjects label with the current teacher's subjects
            self.label_subject_list.setText(', '.join(current_teacher.subjects))
        else:
            self.label_table_title.setText("No teacher is selected")
            self.label_subject_list.setText("No subjects")
        print("Selected item:", selected_text)

    def buttonAddTeacherClicked(self):
        class TeacherDialog(QDialog):
            def __init__(self):
                super().__init__()

                self.dialog_teacher_name = ""

                self.setWindowTitle("Enter Teacher's Name")
                self.setWindowIcon(QIcon("icon.png"))
                self.layout = QVBoxLayout()
                self.label = QLabel("Enter Teacher's Name:")
                self.lineedit = QLineEdit()
                self.button = QPushButton("Add Teacher")
                self.button.clicked.connect(self.get_teacher_name)
                self.layout.addWidget(self.label)
                self.layout.addWidget(self.lineedit)
                self.layout.addWidget(self.button)
                self.setLayout(self.layout)

            def get_teacher_name(self):
                name = self.lineedit.text()
                self.dialog_teacher_name = name
                self.accept()

        dialog = TeacherDialog()
        dialog.setWindowModality(Qt.ApplicationModal)
        dialog.exec_()

        # Initialize the teacher's availability to be all False (i.e., not available)
        teacher = Teacher(dialog.dialog_teacher_name, [[False] * 5 for _ in range(5)], [])

        # Add teacher
        if teacher is not None:
            teachers.append(teacher)
            self.list_widget_teachers.addItem(teacher.name)
            self.list_widget_teachers.setCurrentRow(len(teachers) - 1)  # Select the newly added teacher
            self.label_teacher_quantity.setText(f"## Teachers: {len(teachers)}")

        for t in teachers:
            t.display_info()
            pass

    def getCurrentTeacherIndex(self):
        selected_item = self.list_widget_teachers.currentItem()
        if selected_item is None:  # If no teacher is selected
            return None
        selected_name = selected_item.text()
        for i in range(len(teachers)):
            if teachers[i].name == selected_name:
                return i
        return None  # if no teacher is found

    def check_state_changed(self, state):
        sender = self.sender()
        if sender:
            row = column = -1
            for i in range(self.table_widget.rowCount()):
                for j in range(self.table_widget.columnCount()):
                    if self.table_widget.cellWidget(i, j) == sender:
                        row, column = i, j
                        break

            # Update the corresponding teacher's availability data
            current_teacher_index = self.getCurrentTeacherIndex()
            if current_teacher_index is not None:
                current_teacher = teachers[current_teacher_index]
                current_teacher.availability[row][column] = state == Qt.Checked
            print(f'Checkbox at row {row}, column {column} state changed to {state}')

    def table_cell_clicked(self, row, column):
        checkbox = self.table_widget.cellWidget(row, column)
        if checkbox is not None:
            checkbox.setChecked(not checkbox.isChecked())

        print(f"Cell clicked: Row={row}, Column={column}")

    def buttonAddSubjectClicked(self):
        class SubjectDialog(QDialog):
            def __init__(self):
                super().__init__()

                self.dialog_subject_name = ""

                self.setWindowTitle("Enter Subject's Name")
                self.setWindowIcon(QIcon("icon.png"))
                self.layout = QVBoxLayout()
                self.label = QLabel("Enter Subject's Name:")
                self.lineedit = QLineEdit()
                self.button = QPushButton("Add Subject")
                self.button.clicked.connect(self.get_subject_name)
                self.layout.addWidget(self.label)
                self.layout.addWidget(self.lineedit)
                self.layout.addWidget(self.button)
                self.setLayout(self.layout)

            def get_subject_name(self):
                name = self.lineedit.text()
                self.dialog_subject_name = name
                self.accept()

        dialog = SubjectDialog()
        dialog.setWindowModality(Qt.ApplicationModal)
        dialog.exec_()
        subject = dialog.dialog_subject_name

        # Add subject to the teacher
        current_teacher_index = self.getCurrentTeacherIndex()
        if current_teacher_index is not None:
            current_teacher = teachers[current_teacher_index]
            current_teacher.add_subject(subject)
            self.label_subject_list.setText(', '.join(current_teacher.subjects))



class Ui2(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui2, self).__init__()
        uic.loadUi('groups_cabinets.ui', self)

        self.groups = []
        self.rooms = []

        self.button_teachers = self.findChild(QtWidgets.QToolButton, 'navigation_buttonAvailability')
        self.button_teachers.clicked.connect(self.buttonTeachersClicked)
        self.button_generate = self.findChild(QtWidgets.QToolButton, 'navigation_buttonGenerateTimetable')
        self.button_generate.clicked.connect(self.buttonGenerateClicked)

        self.button_add_group = self.findChild(QtWidgets.QPushButton, 'groups_buttonAddGroup')
        self.button_add_group.clicked.connect(self.addGroup)

        self.button_add_room = self.findChild(QtWidgets.QPushButton, 'cabinets_buttonAddCabinet')
        self.button_add_room.clicked.connect(self.addRoom)

        self.table_groups = self.findChild(QtWidgets.QTableView, 'groups_tableGroups')
        self.groups_model = QStandardItemModel(self.table_groups)
        self.table_groups.horizontalHeader().setStretchLastSection(True)
        self.groups_model.itemChanged.connect(self.updateGroup)

        self.table_rooms = self.findChild(QtWidgets.QTableView, 'cabinets_tableCabinets')
        self.rooms_model = QStandardItemModel(self.table_rooms)
        self.table_rooms.horizontalHeader().setStretchLastSection(True)
        self.rooms_model.itemChanged.connect(self.updateRoom)

        self.table_groups.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.table_rooms.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)

        font = self.table_groups.horizontalHeader().font()
        font.setBold(True)
        self.table_groups.horizontalHeader().setFont(font)
        self.table_groups.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.table_groups.setGridStyle(Qt.SolidLine)

        font = self.table_rooms.horizontalHeader().font()
        font.setBold(True)
        self.table_rooms.horizontalHeader().setFont(font)
        self.table_rooms.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.table_rooms.setGridStyle(Qt.SolidLine)

        self.show()

    def addGroup(self):
        text, ok = QInputDialog.getText(self, 'Add Group', 'Enter group name:')
        if ok:
            size, ok = QInputDialog.getInt(self, 'Add Group', 'Enter group size:')
            if ok:
                self.groups.append(Group(text, size))
                self.updateGroupTable()

    def addRoom(self):
        text, ok = QInputDialog.getText(self, 'Add Room', 'Enter room name:')
        if ok:
            capacity, ok = QInputDialog.getInt(self, 'Add Room', 'Enter room capacity:')
            if ok:
                self.rooms.append(Room(text, capacity))
                self.updateRoomTable()

    def updateGroupTable(self):
        self.groups_model.clear()
        self.groups_model.setHorizontalHeaderLabels(['Group Name', 'Size'])
        for group in self.groups:
            item1 = QStandardItem(group.name)
            item1.setTextAlignment(Qt.AlignCenter)
            item2 = QStandardItem(str(group.size))
            item2.setTextAlignment(Qt.AlignCenter)
            self.groups_model.appendRow([item1, item2])
        self.table_groups.setModel(self.groups_model)

    def updateRoomTable(self):
        self.rooms_model.clear()
        self.rooms_model.setHorizontalHeaderLabels(['Room Name', 'Capacity'])
        for room in self.rooms:
            item1 = QStandardItem(room.name)
            item1.setTextAlignment(Qt.AlignCenter)
            item2 = QStandardItem(str(room.capacity))
            item2.setTextAlignment(Qt.AlignCenter)
            self.rooms_model.appendRow([item1, item2])
        self.table_rooms.setModel(self.rooms_model)

    def updateGroup(self, item):
        row = item.row()
        column = item.column()
        value = item.text()
        group = self.groups[row]
        if column == 0:
            group.name = value
        elif column == 1:
            group.size = int(value)

    def updateRoom(self, item):
        row = item.row()
        column = item.column()
        value = item.text()
        room = self.rooms[row]
        if column == 0:
            room.name = value
        elif column == 1:
            room.capacity = int(value)

        self.printRooms()

    def printRooms(self):
        for room in self.rooms:
            print(room.name, room.capacity)

    def buttonTeachersClicked(self):
        window1.show()
        window2.hide()

    def buttonGenerateClicked(self):
        window3.show()
        window2.hide()




class Ui3(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui3, self).__init__()
        uic.loadUi('generate.ui', self)

        self.spinBox_pairs_in_a_row = self.findChild(QtWidgets.QSpinBox, 'generate_spinBoxPairsInARow')
        self.spinBox_output = self.findChild(QtWidgets.QSpinBox, 'generate_spinBoxOutput')

        self.button_generate_timetable = self.findChild(QtWidgets.QPushButton, 'generate_buttonGenerate')
        self.button_generate_timetable.clicked.connect(self.generate_timetable)

        self.button_teachers = self.findChild(QtWidgets.QToolButton, 'navigation_buttonAvailability')
        self.button_teachers.clicked.connect(self.buttonTeachersClicked)
        self.button_groups = self.findChild(QtWidgets.QToolButton, 'navigation_buttonGroupsAndRooms')
        self.button_groups.clicked.connect(self.buttonGroupsClicked)

        self.show()

    def generate_timetable(self):
        print("generate clicked")
        pairs_in_a_row = self.spinBox_pairs_in_a_row.value()
        # genetic_algorithm = GeneticAlgorithm(teachers, window2.rooms, window2.groups, 50)
        # schedule = genetic_algorithm.generate()
        # genetic_algorithm.print_schedule(schedule)

    def buttonTeachersClicked(self):
        window1.show()
        window3.hide()

    def buttonGroupsClicked(self):
        window2.show()
        window3.hide()



teachers = []
# rooms and groups should be taken from window2






app = QtWidgets.QApplication(sys.argv)
window1 = Ui1()
window2 = Ui2()
window2.hide()
window3 = Ui3()
window3.hide()



app.exec_()



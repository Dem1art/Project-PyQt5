import sys
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui, QtWidgets
import sqlite3
import datetime as dt


class MainWindow(QMainWindow):  # Класс реализующий основное окно
    def __init__(self):
        super().__init__()
        self.setupUi(self)  # создание интерфейса

        self.add_button.clicked.connect(self.run)  # кнопка добавления заметки

        self.update_button.clicked.connect(self.update)  # кнопка обновления

        self.listWidget.itemSelectionChanged.connect(
            lambda: self.openShowWindow(self.listWidget.currentRow()))  # кнопки внутри списка заметок

        self.search_button.clicked.connect(self.open_search_form)

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(301, 613)
        MainWindow.setMinimumSize(QtCore.QSize(301, 613))
        MainWindow.setMaximumSize(QtCore.QSize(301, 613))
        MainWindow.setBaseSize(QtCore.QSize(301, 613))
        font = QtGui.QFont()
        font.setPointSize(9)
        MainWindow.setFont(font)
        MainWindow.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(
            "png-transparent-computer-icons-post-it-note-notes-icon-rectangle-orange-notes.png"),
                       QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setAutoFillBackground(False)
        MainWindow.setStyleSheet("background-color: rgb(0, 85, 127);")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 10, 281, 61))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.search_button = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.search_button.setStyleSheet("background-color: rgb(217, 217, 217);")
        self.search_button.setObjectName("search_button")
        self.verticalLayout.addWidget(self.search_button)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.add_button = QtWidgets.QPushButton(self.centralwidget)
        self.add_button.setGeometry(QtCore.QRect(230, 540, 61, 61))
        self.add_button.setMinimumSize(QtCore.QSize(61, 61))
        self.add_button.setMaximumSize(QtCore.QSize(61, 61))
        self.add_button.setBaseSize(QtCore.QSize(61, 61))
        self.add_button.setStyleSheet("font: 24pt \"MS Shell Dlg 2\";\n"
                                      "background-color: rgb(217, 217, 217);")
        self.add_button.setObjectName("add_button")
        self.update_button = QtWidgets.QPushButton(self.centralwidget)
        self.update_button.setGeometry(QtCore.QRect(10, 560, 75, 23))
        self.update_button.setStyleSheet("background-color: rgb(217, 217, 217);")
        self.update_button.setObjectName("update_button")
        self.listWidget = QtWidgets.QListWidget(self.centralwidget)
        self.listWidget.setGeometry(QtCore.QRect(10, 50, 281, 481))
        self.listWidget.setStyleSheet("background-color: rgb(216, 255, 255);")
        self.listWidget.setVerticalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)
        self.listWidget.setHorizontalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)
        self.listWidget.setObjectName("listWidget")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Заметки"))
        self.search_button.setText(_translate("MainWindow", "Поиск"))
        self.add_button.setText(_translate("MainWindow", "+"))
        self.update_button.setText(_translate("MainWindow", "Обновить"))
        self.listWidget.setSortingEnabled(False)

    def run(self):
        name, ok_pressed = QInputDialog.getText(self, "Имя файла",  # добавление заметки(файла) через диологовое окн
                                                "Как назвать файл?")
        if ok_pressed:
            self.file_form = FileForm(self, name)  # открываем форму создания заметки
            self.file_form.show()

    def update(self):  # обновление list
        self.listWidget.clear()
        con = sqlite3.connect("Notes.sqlite")
        # Создание курсора
        cur = con.cursor()
        # Выполнение запроса и получение всех результатов
        self.result = cur.execute("""SELECT id, name FROM Notes""").fetchall()
        i = 0
        for elem in self.result:
            self.elem = str(elem[1])
            i += 1
            self.listWidget.addItem(f'{i}) {self.elem}')

    def open_search_form(self):
        self.search_form = SearchForm()
        self.search_form.show()

    def openShowWindow(self, row):  # открытие формы редакции
        con = sqlite3.connect("Notes.sqlite")
        # Создание курсора
        cur = con.cursor()
        # Выполнение запроса и получение всех результатов
        result = cur.execute("""SELECT * FROM Notes""").fetchall()
        con.close()
        if result:
            self.editorial_form = EditorialForm(self, result[row][0])
            self.editorial_form.show()


class FileForm(QWidget):  # форма создания заметки
    def __init__(self, *args):
        super().__init__()
        self.setupUi(self)
        self.typer = 7  # тип заметки

        self.file_name.setText(f'{args[-1]}')  # строка с именем заметки

        self.add_button2.clicked.connect(self.add_note)  # кнопка добавления

        self.type_button.clicked.connect(self.type)  # кнопка выбора типа заметки

    def setupUi(self, File_form):
        File_form.setObjectName("File_form")
        File_form.resize(301, 613)
        File_form.setMinimumSize(QtCore.QSize(301, 613))
        File_form.setMaximumSize(QtCore.QSize(301, 613))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(
            "png-transparent-computer-icons-post-it-note-notes-icon-rectangle-orange-notes.png"),
            QtGui.QIcon.Normal, QtGui.QIcon.Off)
        File_form.setWindowIcon(icon)
        File_form.setStyleSheet("background-color: rgb(0, 85, 127);")
        self.add_button2 = QtWidgets.QPushButton(File_form)
        self.add_button2.setGeometry(QtCore.QRect(230, 540, 61, 61))
        self.add_button2.setMinimumSize(QtCore.QSize(61, 61))
        self.add_button2.setMaximumSize(QtCore.QSize(61, 61))
        self.add_button2.setBaseSize(QtCore.QSize(61, 61))
        font = QtGui.QFont()
        font.setPointSize(24)
        self.add_button2.setFont(font)
        self.add_button2.setStyleSheet("background-color: rgb(217, 217, 217);")
        self.add_button2.setObjectName("add_button2")
        self.label = QtWidgets.QLabel(File_form)
        self.label.setGeometry(QtCore.QRect(10, 70, 47, 13))
        self.label.setStyleSheet("color: rgb(255, 255, 255);")
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(File_form)
        self.label_2.setGeometry(QtCore.QRect(10, 10, 71, 16))
        self.label_2.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_2.setObjectName("label_2")
        self.file_name = QtWidgets.QLineEdit(File_form)
        self.file_name.setGeometry(QtCore.QRect(12, 40, 111, 20))
        self.file_name.setStyleSheet("background-color: rgb(216, 255, 255);")
        self.file_name.setObjectName("file_name")
        self.textEdit = QtWidgets.QTextEdit(File_form)
        self.textEdit.setGeometry(QtCore.QRect(13, 100, 271, 431))
        self.textEdit.setStyleSheet("background-color: rgb(216, 255, 255);")
        self.textEdit.setObjectName("textEdit")
        self.type_button = QtWidgets.QPushButton(File_form)
        self.type_button.setGeometry(QtCore.QRect(190, 40, 91, 23))
        self.type_button.setStyleSheet("background-color: rgb(217, 217, 217);")
        self.type_button.setObjectName("type_button")

        self.retranslateUi(File_form)
        QtCore.QMetaObject.connectSlotsByName(File_form)

    def retranslateUi(self, File_form):
        _translate = QtCore.QCoreApplication.translate
        File_form.setWindowTitle(_translate("File_form", "Добавить"))
        self.add_button2.setText(_translate("File_form", "+"))
        self.label.setText(_translate("File_form", "Текст"))
        self.label_2.setText(_translate("File_form", "Имя заметки"))
        self.type_button.setText(_translate("File_form", "Тип заметки"))

    def add_note(self):  # добавление заметки в бд
        name = self.file_name.text()
        text = self.textEdit.toPlainText()

        date = dt.datetime.now().date()  # дата создания заметки
        notification = dt.datetime.now().date()  # дата последнего изменения

        # Подключение к БД
        con = sqlite3.connect('Notes.sqlite')
        # Создание курсора
        cur = con.cursor()
        # Выполнение запроса
        cur.execute(f"""INSERT INTO Notes(name, text, type, date_of_creation, notification) VALUES('{name}', 
        '{text}', '{self.typer}', '{date}', '{notification}')""")
        con.commit()
        con.close()
        self.close()

    def type(self):  # определение типа заметки
        typer, ok_pressed = QInputDialog.getItem(
            self, "Выберите тип заметки", "Типы",
            ("Работа", "Почта", "Список", "Фильмы", "Учёба", "Дела", "Без типа"), 1, False)
        if ok_pressed:
            self.type_button.setText(typer)
        con = sqlite3.connect("Notes.sqlite")
        cur = con.cursor()
        result = cur.execute(f"""SELECT id FROM Types
WHERE type='{typer}'""")
        self.typer = result.fetchone()[0]
        con.close()


class SearchForm(QWidget):  # форма поиска
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.search = 'Поиск по содержанию'  # текст кнопки типа поиска
        self.text = self.lineEdit.text()  # текст введённый в поле ввода
        self.result = 7  # список заметок содержащихся в листе
        self.text_result_list = ''

        self.search_button.clicked.connect(self.update_list)  # кнопка обнавления листа

        self.search_type_button.clicked.connect(self.search_type)  # кнопка для выбора типа поиска

        self.result_list.itemSelectionChanged.connect(lambda: self.openShowWindow())

    def setupUi(self, Search_form):
        Search_form.setObjectName("Search_form")
        Search_form.resize(301, 613)
        Search_form.setMinimumSize(QtCore.QSize(301, 613))
        Search_form.setMaximumSize(QtCore.QSize(301, 613))
        Search_form.setBaseSize(QtCore.QSize(301, 613))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(
            "png-transparent-computer-icons-post-it-note-notes-icon-rectangle-orange-notes.png"),
                       QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Search_form.setWindowIcon(icon)
        Search_form.setStyleSheet("background-color: rgb(0, 85, 127);")
        self.search_button = QtWidgets.QPushButton(Search_form)
        self.search_button.setGeometry(QtCore.QRect(220, 10, 75, 21))
        self.search_button.setStyleSheet("background-color: rgb(217, 217, 217);")
        self.search_button.setObjectName("search_button")
        self.lineEdit = QtWidgets.QLineEdit(Search_form)
        self.lineEdit.setGeometry(QtCore.QRect(10, 10, 211, 21))
        self.lineEdit.setStyleSheet("background-color: rgb(216, 255, 255);")
        self.lineEdit.setText("")
        self.lineEdit.setObjectName("lineEdit")
        self.result_list = QtWidgets.QListWidget(Search_form)
        self.result_list.setGeometry(QtCore.QRect(10, 50, 281, 521))
        self.result_list.setStyleSheet("background-color: rgb(216, 255, 255);")
        self.result_list.setObjectName("result_list")
        self.search_type_button = QtWidgets.QPushButton(Search_form)
        self.search_type_button.setGeometry(QtCore.QRect(10, 580, 281, 23))
        self.search_type_button.setStyleSheet("background-color: rgb(217, 217, 217);")
        self.search_type_button.setObjectName("search_type_button")

        self.retranslateUi(Search_form)
        QtCore.QMetaObject.connectSlotsByName(Search_form)

    def retranslateUi(self, Search_form):
        _translate = QtCore.QCoreApplication.translate
        Search_form.setWindowTitle(_translate("Search_form", "Поиск"))
        self.search_button.setText(_translate("Search_form", " Поиск"))
        self.lineEdit.setPlaceholderText(_translate("Search_form", "Поиск"))
        self.search_type_button.setText(_translate("Search_form", "Поиск по содержанию"))

    def update_list(self):  # функция обнавления
        self.result_list.clear()
        self.text = self.lineEdit.text()
        con = sqlite3.connect("Notes.sqlite.sqlite")
        # Создание курсора
        cur = con.cursor()
        if self.search == 'Поиск по содержанию':
            # Выполнение запроса и получение всех результатов
            self.result = cur.execute(f"""SELECT id, name FROM Notes
            WHERE text like '%{self.text}%'""").fetchall()
            for elem in self.result:
                self.result_list.addItem(f'{elem[0]}) {elem[1]}')
        if self.search == 'Поиск по названию':
            # Выполнение запроса и получение всех результатов
            self.result = cur.execute(f"""SELECT id, name FROM Notes
                        WHERE name like '%{self.text}%'""").fetchall()
            for elem in self.result:
                self.result_list.addItem(f'{elem[0]}) {elem[1]}')
        if self.search == 'Поиск по типу заметки':
            # Выполнение запроса и получение всех результатов
            self.result = cur.execute(f"""SELECT id, name FROM Notes
            WHERE type=(
            SELECT id FROM Types
            WHERE type='{self.text}')""").fetchall()
            for elem in self.result:
                self.result_list.addItem(f'{elem[0]}) {elem[1]}')
        con.close()

    def search_type(self):  # функция для выбора типа поиска
        search, ok_pressed = QInputDialog.getItem(
            self, "Выберите тип заметки", "Типы",
            ("Поиск по содержанию", "Поиск по названию", "Поиск по типу заметки"), 1, False)
        if ok_pressed:
            self.search_type_button.setText(search)
            self.search = search

    def openShowWindow(self):  # открыть форму редактирования
        self.text_item = ''
        self.text_item = [item.text() for item in self.result_list.selectedItems()]  # текст с кнопки листа
        if len(self.text_item) != 0:
            row = self.text_item[0].split(')')
            row = int(row[0])

            self.editorial_form = EditorialForm(self, row)
            self.editorial_form.show()


class EditorialForm(QWidget):  # форма редакции
    def __init__(self, *args):
        super().__init__()
        self.setupUi(self)
        self.id_note = args[1]  # номер заметки
        self.typer = 7

        con = sqlite3.connect("Notes.sqlite")
        # Создание курсора
        cur = con.cursor()
        # Выполнение запроса и получение всех результатов
        result = cur.execute(f"""SELECT * FROM Notes
        WHERE id={self.id_note}""").fetchall()

        self.file_name.setText(result[0][1])  # название заметки
        self.textEdit.setText(result[0][2])  # текст заметки
        self.label_3.setText(f'Дата создания: {result[0][4]}')  # дата создания заметки
        self.label_4.setText(f'Последнее изменение: {result[0][5]}')  # дата последнего изменения заметки

        typ = cur.execute(f"""SELECT type FROM Types
                WHERE id={result[0][3]}""").fetchall()

        self.type_button.setText(typ[0][0])  # тип заметки
        con.close()

        self.type_button.clicked.connect(self.type)  # изменение типа заметки

        self.confirming_button.clicked.connect(self.confirming)  # кнопка подтверждения изменения

        self.delete_button.clicked.connect(self.delete_note)

    def setupUi(self, Form_editorial):
        Form_editorial.setObjectName("Form_editorial")
        Form_editorial.resize(301, 613)
        Form_editorial.setMinimumSize(QtCore.QSize(301, 613))
        Form_editorial.setMaximumSize(QtCore.QSize(301, 613))
        Form_editorial.setBaseSize(QtCore.QSize(301, 613))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(
            "png-transparent-computer-icons-post-it-note-notes-icon-rectangle-orange-notes.png"),
            QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Form_editorial.setWindowIcon(icon)
        Form_editorial.setStyleSheet("background-color: rgb(0, 85, 127);")
        self.label = QtWidgets.QLabel(Form_editorial)
        self.label.setGeometry(QtCore.QRect(10, 70, 47, 13))
        self.label.setStyleSheet("color: rgb(255, 255, 255);")
        self.label.setObjectName("label")
        self.delete_button = QtWidgets.QPushButton(Form_editorial)
        self.delete_button.setGeometry(QtCore.QRect(10, 540, 101, 31))
        self.delete_button.setStyleSheet("background-color: rgb(217, 217, 217);")
        self.delete_button.setObjectName("delete_button")
        self.label_2 = QtWidgets.QLabel(Form_editorial)
        self.label_2.setGeometry(QtCore.QRect(10, 10, 71, 16))
        self.label_2.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_2.setObjectName("label_2")
        self.file_name = QtWidgets.QLineEdit(Form_editorial)
        self.file_name.setGeometry(QtCore.QRect(10, 40, 113, 20))
        self.file_name.setStyleSheet("background-color: rgb(216, 255, 255);")
        self.file_name.setObjectName("file_name")
        self.textEdit = QtWidgets.QTextEdit(Form_editorial)
        self.textEdit.setGeometry(QtCore.QRect(13, 100, 271, 431))
        self.textEdit.setStyleSheet("background-color: rgb(216, 255, 255);")
        self.textEdit.setObjectName("textEdit")
        self.confirming_button = QtWidgets.QPushButton(Form_editorial)
        self.confirming_button.setGeometry(QtCore.QRect(180, 540, 101, 31))
        self.confirming_button.setStyleSheet("background-color: rgb(217, 217, 217);")
        self.confirming_button.setObjectName("confirming_button")
        self.type_button = QtWidgets.QPushButton(Form_editorial)
        self.type_button.setGeometry(QtCore.QRect(190, 40, 91, 23))
        self.type_button.setStyleSheet("background-color: rgb(217, 217, 217);")
        self.type_button.setObjectName("type_button")
        self.label_3 = QtWidgets.QLabel(Form_editorial)
        self.label_3.setGeometry(QtCore.QRect(100, 70, 161, 16))
        self.label_3.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(Form_editorial)
        self.label_4.setGeometry(QtCore.QRect(10, 580, 271, 16))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 85, 127))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 85, 127))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 85, 127))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 85, 127))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 85, 127))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 85, 127))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 85, 127))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 85, 127))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 85, 127))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
        self.label_4.setPalette(palette)
        self.label_4.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_4.setObjectName("label_4")

        self.retranslateUi(Form_editorial)
        QtCore.QMetaObject.connectSlotsByName(Form_editorial)

    def retranslateUi(self, Form_editorial):
        _translate = QtCore.QCoreApplication.translate
        Form_editorial.setWindowTitle(_translate("Form_editorial", "Редактировать"))
        self.label.setText(_translate("Form_editorial", "Текст"))
        self.delete_button.setText(_translate("Form_editorial", "Удалить заметку"))
        self.label_2.setText(_translate("Form_editorial", "Имя заметки"))
        self.confirming_button.setText(_translate("Form_editorial", "Подтвердить"))
        self.type_button.setText(_translate("Form_editorial", "Тип заметки"))
        self.label_3.setText(_translate("Form_editorial", "TextLabel"))
        self.label_4.setText(_translate("Form_editorial", "TextLabel"))

    def type(self):  # определение типа заметки
        typer, ok_pressed = QInputDialog.getItem(
            self, "Выберите тип заметки", "Типы",
            ("Работа", "Почта", "Список", "Фильмы", "Учёба", "Дела", "Без типа"), 1, False)
        if ok_pressed:
            self.type_button.setText(typer)
        con = sqlite3.connect("Notes.sqlite")
        cur = con.cursor()
        result = cur.execute(f"""SELECT id FROM Types
WHERE type='{typer}'""")
        self.typer = result.fetchone()[0]
        con.close()

    def confirming(self):  # добавление заметки в бд
        name = self.file_name.text()
        text = self.textEdit.toPlainText()

        notification = dt.datetime.now().date()  # дата последнего изменения

        # Подключение к БД
        con = sqlite3.connect('Notes.sqlite')
        # Создание курсора
        cur = con.cursor()
        # Выполнение запроса
        cur.execute(f"""UPDATE Notes
        SET name = '{name}'
        WHERE id = {self.id_note}""")
        con.commit()

        cur.execute(f"""UPDATE Notes
                SET text = '{text}'
                WHERE id = {self.id_note}""")
        con.commit()

        cur.execute(f"""UPDATE Notes
                        SET type = '{self.typer}'
                        WHERE id = {self.id_note}""")
        con.commit()

        cur.execute(f"""UPDATE Notes
                        SET notification = '{notification}'
                        WHERE id = {self.id_note}""")
        con.commit()
        con.close()
        self.close()

    def delete_note(self):  # удаление заметки
        answer, ok_pressed = QInputDialog.getText(self, "Подтверждение удаления",
                                                  "Вы точно хотите удалить заметку?")
        if ok_pressed:
            if answer.lower() == 'да':
                con = sqlite3.connect("Notes.sqlite")
                # Создание курсора
                cur = con.cursor()
                # Выполнение запроса и получение всех результатов
                cur.execute(f"""DELETE FROM Notes
                        WHERE id={self.id_note}""").fetchall()
                con.commit()
                con.close()
                self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec())

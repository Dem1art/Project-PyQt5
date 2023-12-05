import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
import sqlite3
import datetime as dt


class Main_window(QMainWindow):  # Класс реализующий основное окно
    def __init__(self):
        super().__init__()
        uic.loadUi('Main_window.ui', self)

        self.add_button.clicked.connect(self.run)  # кнопка добавления заметки

        self.update_button.clicked.connect(self.update)  # кнопка обновления

        self.listWidget.itemSelectionChanged.connect(lambda: self.openShowWindow())  # кнопки внутри списка заметок

    def run(self):
        name, ok_pressed = QInputDialog.getText(self, "Имя файла",  # добавление заметки(файла) через диологовое окн
                                                "Как назвать файл?")
        if ok_pressed:
            self.file_form = File_form(self, name)  # открываем форму создания заметки
            self.file_form.show()

    def update(self):  # обновление list
        self.listWidget.clear()
        con = sqlite3.connect("Notes_copy.sqlite")
        # Создание курсора
        cur = con.cursor()
        # Выполнение запроса и получение всех результатов
        self.result = cur.execute("""SELECT * FROM Notes""").fetchall()
        for elem in self.result:
            self.elem = str(elem[1])
            self.listWidget.addItem(self.elem)

    def openShowWindow(self):  # открытие формы редакции
        print('puk')


class File_form(QWidget):
    def __init__(self, *args):
        super().__init__()
        uic.loadUi('File_form.ui', self)
        self.typer = 0  # тип заметки

        self.file_name.setText(f'{args[-1]}')  # строка с именем заметки

        self.add_button2.clicked.connect(self.add_note)  # кнопка добавления

        self.type_button.clicked.connect(self.type)  # кнопка выбора типа заметки

    def add_note(self):  # добавление заметки в бд
        name = self.file_name.text()
        text = self.textEdit.toPlainText()

        date = dt.datetime.now().date()  # дата создания заметки
        notification = dt.datetime.now().date()

        # Подключение к БД
        con = sqlite3.connect('Notes_copy.sqlite')
        # Создание курсора
        cur = con.cursor()
        # Выполнение запроса
        if self.typer == 0 or self.typer == 7:
            cur.execute(f"""INSERT INTO Notes(name, text, date_of_creation, notification) VALUES('{name}', '{text}', '{date}', '{notification}')""")
        else:
            cur.execute(f"""INSERT INTO Notes(name, text, type, date_of_creation, notification) VALUES('{name}', '{text}', '{self.typer}', '{date}', '{notification}')""")
        con.commit()
        con.close()
        self.close()

    def type(self):
        typer, ok_pressed = QInputDialog.getItem(
            self, "Выберите тип заметки", "Типы",
            ("Работа", "Почта", "Список", "Фильмы", "Учёба", "Дела", "Без типа"), 1, False)
        if ok_pressed:
            self.type_button.setText(typer)
        con = sqlite3.connect("Notes_copy.sqlite")
        cur = con.cursor()
        result = cur.execute(f"""SELECT id FROM Types
WHERE type='{typer}'""")
        self.typer = result.fetchone()[0]
        con.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Main_window()
    ex.show()
    sys.exit(app.exec())
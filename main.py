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


    def run(self):
        name, ok_pressed = QInputDialog.getText(self, "Имя файла",  # добавление заметки(файла) через диологовое окн
                                                "Как назвать файл?")
        if ok_pressed:
            self.file_form = File_form(self, name)
            self.file_form.show()


class File_form(QWidget):
    def __init__(self, *args):
        super().__init__()
        uic.loadUi('File_form.ui', self)

        self.file_name.setText(f'{args[-1]}')

        self.add_button.clicked.connect(self.add_note)

    def add_note(self):
        name = self.file_name.text()
        text = self.textEdit.toPlainText()
        date = dt.datetime.now().date()  # дата создания заметки

        # Подключение к БД
        con = sqlite3.connect('Notes_copy.sqlite')
        # Создание курсора
        cur = con.cursor()
        # Выполнение запроса
        cur.execute(f"""INSERT INTO Notes(name, text, date_of_creation) VALUES('{name}', '{text}', '{date}')""")
        con.commit()
        con.close()

        self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Main_window()
    ex.show()
    sys.exit(app.exec())
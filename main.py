import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QInputDialog
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
            with open(f'{name}.txt', 'w', encoding='utf-8') as f:  # создание файла
                f.close()

            date = dt.datetime.now().date()  # дата создания заметки

            # Подключение к БД
            con = sqlite3.connect('Notes_copy.sqlite')
            # Создание курсора
            cur = con.cursor()
            # Выполнение запроса
            cur.execute(f"""INSERT INTO Notes(name, date_of_creation) VALUES('{name}', '{date}')""")
            con.commit()
            con.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Main_window()
    ex.show()
    sys.exit(app.exec())
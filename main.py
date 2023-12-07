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

        self.listWidget.itemSelectionChanged.connect(lambda: self.openShowWindow(self.listWidget.currentRow()))  # кнопки внутри списка заметок

        self.search_button.clicked.connect(self.open_search_form)

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
        self.result = cur.execute("""SELECT id, name FROM Notes""").fetchall()
        i = 0
        for elem in self.result:
            self.elem = str(elem[1])
            i += 1
            self.listWidget.addItem(f'{i}) {self.elem}')

    def open_search_form(self):
        self.search_form = Search_form()
        self.search_form.show()

    def openShowWindow(self, row):  # открытие формы редакции
        con = sqlite3.connect("Notes_copy.sqlite")
        # Создание курсора
        cur = con.cursor()
        # Выполнение запроса и получение всех результатов
        result = cur.execute("""SELECT * FROM Notes""").fetchall()
        con.close()
        self.editorial_form = Editorial_form(self, result[row][0])
        self.editorial_form.show()



class File_form(QWidget):  # форма создания заметки
    def __init__(self, *args):
        super().__init__()
        uic.loadUi('File_form.ui', self)
        self.typer = 7  # тип заметки

        self.file_name.setText(f'{args[-1]}')  # строка с именем заметки

        self.add_button2.clicked.connect(self.add_note)  # кнопка добавления

        self.type_button.clicked.connect(self.type)  # кнопка выбора типа заметки

    def add_note(self):  # добавление заметки в бд
        name = self.file_name.text()
        text = self.textEdit.toPlainText()

        date = dt.datetime.now().date()  # дата создания заметки
        notification = dt.datetime.now().date()  # дата последнего изменения

        # Подключение к БД
        con = sqlite3.connect('Notes_copy.sqlite')
        # Создание курсора
        cur = con.cursor()
        # Выполнение запроса
        cur.execute(f"""INSERT INTO Notes(name, text, type, date_of_creation, notification) VALUES('{name}', '{text}', '{self.typer}', '{date}', '{notification}')""")
        con.commit()
        con.close()
        self.close()

    def type(self):  # определение типа заметки
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


class Search_form(QWidget):  # форма поиска
    def __init__(self):
        super().__init__()
        uic.loadUi('Search_form.ui', self)
        self.search = 'Поиск по содержанию'  # текст кнопки типа поиска
        self.text = self.lineEdit.text()  # текст введённый в поле ввода
        self.result = 7  # список заметок содержащихся в листе
        self.text_result_list = ''

        self.search_button.clicked.connect(self.update_list)  # кнопка обнавления листа

        self.search_type_button.clicked.connect(self.search_type)  # кнопка для выбора типа поиска

        self.result_list.itemSelectionChanged.connect(lambda: self.openShowWindow(str(self.result_list.currentTextChanged())))

    def update_list(self):  # функция обнавления
        self.result_list.clear()
        self.text = self.lineEdit.text()
        con = sqlite3.connect("Notes_copy.sqlite")
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

    def openShowWindow(self, row):  # открыть форму редактирования
        row = row.splite()[0]
        row = int(row[:-1])
        self.editorial_form = Editorial_form(self, row)
        self.editorial_form.show()


class Editorial_form(QWidget):  # форма редакции
    def __init__(self, *args):
        super().__init__()
        uic.loadUi('Editorial_form.ui', self)
        self.id_note = args[1]  # номер заметки
        self.typer = 7

        con = sqlite3.connect("Notes_copy.sqlite")
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

    def type(self):  # определение типа заметки
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

    def confirming(self):  # добавление заметки в бд
        name = self.file_name.text()
        text = self.textEdit.toPlainText()

        notification = dt.datetime.now().date()  # дата последнего изменения

        # Подключение к БД
        con = sqlite3.connect('Notes_copy.sqlite')
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
                con = sqlite3.connect("Notes_copy.sqlite")
                # Создание курсора
                cur = con.cursor()
                # Выполнение запроса и получение всех результатов
                result = cur.execute(f"""DELETE FROM Notes
                        WHERE id={self.id_note}""").fetchall()
                con.commit()
                con.close()
                self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Main_window()
    ex.show()
    sys.exit(app.exec())
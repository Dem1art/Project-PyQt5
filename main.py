import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QInputDialog
from PyQt5 import uic


class Main_window(QMainWindow):  # Класс реализующий основное окно
    def __init__(self):
        super().__init__()
        uic.loadUi('Main_window.ui', self)


        self.add_button.clicked.connect(self.run)  # кнопка добавления заметки


    def run(self):
        name, ok_pressed = QInputDialog.getText(self, "Имя файла",  # добавление заметки(файла) через диологовое окн
                                                "Как назвать файл?")
        if ok_pressed:
            with open(name, 'w', encoding='utf-8') as f:  # создание файла
                text = sys.stdin.read()
                f.write(text)
                f.close()





if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Main_window()
    ex.show()
    sys.exit(app.exec())
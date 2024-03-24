from PySide6.QtCore import Qt, QXmlStreamReader, QFile
from PySide6.QtWidgets import QApplication, QMainWindow, QMessageBox, QFileDialog
from lxml import etree
from ui_mainwindow import Ui_MainWindow


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, app):
        super().__init__()
        self.setupUi(self)
        self.app = app
        self.open_action.triggered.connect(self.open_file)
        self.xml_data = None

    # open xml file
    def open_file(self):
        file_path, _ = QFileDialog.getOpenFileName(filter="XML Files (*.xml)")
        file = QFile(file_path)

        # Відкрити файл
        if not file.open(QFile.ReadOnly):
            return

        # Створити дерево lxml
        context = etree.iterparse(file_path, events=("start", "end"))

        # Для кожної події
        for event, element in context:
            # Вивести ім'я тегу
            print(f"Назва елемента: {element.tag}")

            # Якщо це подія "start", вивести атрибути
            if event == "start":
                for attribute in element.attrib:
                    print(f"Атрибут: {attribute} = {element.attrib[attribute]}")

            # Якщо це подія "end", вивести текстовий вміст
            if event == "end":
                print(f"Вміст елемента: {element.text}")

        file.close()
        print("File closed")

from PySide6.QtCore import Qt, QXmlStreamReader, QFile
from PySide6.QtGui import QStandardItemModel, QStandardItem
from PySide6.QtWidgets import QApplication, QMainWindow, QMessageBox, QFileDialog
from bs4 import BeautifulSoup
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

        if file_path:
            # Завантажити файл
            with open(file_path, "r", encoding="windows-1251") as f:
                soup = BeautifulSoup(f.read(), "lxml")

        # Знайти всі теги
        tags = soup.find_all("category")
        categories = []
        products = {}
        # Для кожного тегу
        for tag in tags:
            # Вивести ім'я тегу
            # print(f"Назва елемента: {tag.name}")

            # Вивести текст тегу
            # print(f"Вміст елемента: {tag.text.strip()}")
            category = tag.text.strip()
            categories.append(category)
            products[category] = ["product_1", "product_2", "product_3"]

        # Створити модель даних
        model = MyModel(products)

        # Додати категорії товарів
        for category in categories:
            # Створити вузол для категорії
            category_item = QStandardItem(category)
            category_item.setCheckable(True)

            # Додати товари до категорії
            for product in products[category]:
                product_item = QStandardItem(product)
                product_item.setCheckable(True)
                category_item.appendRow(product_item)

            # Додати вузол категорії до моделі
            model.appendRow(category_item)
        model.setHeaderData(0, Qt.Horizontal, "Категорія")
        self.tree_view.setModel(model)
        print("File closed")


class MyModel(QStandardItemModel):
    def __init__(self, data):
        super().__init__()

        self._data = data

    def flags(self, index):
        flags = super().flags(index)

        if index.isValid():
            flags |= Qt.ItemIsUserCheckable

        return flags

    def data(self, index, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            return self._data[index.row()]

        return super().data(index, role)

    def dataChanged(self, left, right, roles):
        super().dataChanged(left, right, roles)

        if roles & Qt.CheckStateRole:
            # Отримати категорію
            category_index = left.parent()

            # Оновити стан категорії
            if self.itemFromIndex(category_index).checkState() != Qt.Checked:
                self.itemFromIndex(category_index).setCheckState(Qt.Checked)

            # Рекурсивно оновити батьківські категорії
            self._updateParentCheckState(category_index)

    def _updateParentCheckState(self, index):
        if index.parent().isValid():
            parent_item = self.itemFromIndex(index.parent())

            # Якщо всі дочірні елементи
            if all(child.checkState() == Qt.Checked for child in parent_item.children()):
                parent_item.setCheckState(Qt.Checked)
            else:
                parent_item.setCheckState(Qt.PartiallyChecked)

            self._updateParentCheckState(index.parent())

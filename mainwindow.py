from PySide6 import QtGui, QtCore
from PySide6.QtCore import Qt
from PySide6.QtCore import QSortFilterProxyModel
from PySide6.QtGui import QStandardItemModel, QStandardItem
from PySide6.QtWidgets import QMainWindow, QFileDialog
from bs4 import BeautifulSoup
from ui_mainwindow import Ui_MainWindow


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, app):
        super().__init__()
        self.setupUi(self)
        self.app = app

        # Init of table_view_1
        self.source_cat_model = QStandardItemModel()
        header_name = ["Категорія"]
        self.source_cat_model.setHorizontalHeaderLabels(header_name)
        self.source_cat_proxy_model = QSortFilterProxyModel()
        self.source_cat_proxy_model.setSourceModel(self.source_cat_model)
        self.source_cat_proxy_model.setFilterKeyColumn(0)
        self.source_category_table_view.setModel(self.source_cat_proxy_model)
        self.source_category_table_view.resizeColumnsToContents()
        self.source_category_table_view.horizontalHeader().setStretchLastSection(True)
        self.source_category_table_view.horizontalHeader().setDefaultAlignment(Qt.AlignLeft)

        # Init of table_view_2
        self.fin_cat_model = QStandardItemModel()
        self.fin_cat_model.setHorizontalHeaderLabels(header_name)
        self.final_category_table_view.setModel(self.fin_cat_model)
        self.final_category_table_view.resizeColumnsToContents()
        self.final_category_table_view.horizontalHeader().setStretchLastSection(True)
        self.final_category_table_view.horizontalHeader().setDefaultAlignment(Qt.AlignLeft)

        self.search_line_edit.textChanged.connect(self.onTextChanged)

        self.open_action.triggered.connect(self.open_file)
        self.xml_data = None

    def onTextChanged(self, text):
        self.source_cat_proxy_model.setFilterFixedString(text)

    # open xml file
    def open_file(self):
        file_path, _ = QFileDialog.getOpenFileName(filter="XML Files (*.xml)")
        categories = self.parse(file_path)
        for category in categories:
            category_item = QStandardItem(category)
            category_item.setCheckable(True)
            self.source_cat_model.appendRow(category_item)

        print("File closed")

    def parse(self, file_path):
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
        return categories

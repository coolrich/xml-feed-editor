from PySide6 import QtGui, QtCore
from PySide6.QtCore import Qt
from PySide6.QtCore import QSortFilterProxyModel
from PySide6.QtGui import QStandardItemModel, QStandardItem
from PySide6.QtWidgets import QMainWindow, QFileDialog, QAbstractItemView
from bs4 import BeautifulSoup
from ui_mainwindow import Ui_MainWindow


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, app):
        super().__init__()
        self.setupUi(self)
        self.app = app

        # Init of table_view_1
        header_name = ["Категорія"]
        self.source_cat_model = QStandardItemModel()
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
        self.add_cat_push_button.clicked.connect(self.add_category)
        self.delete_cat_push_button.clicked.connect(self.remove_category)

        self.xml_data = None

    def onTextChanged(self, text):
        self.source_cat_proxy_model.setFilterFixedString(text)

    def add_category(self):
        sctv_model = self.source_category_table_view.model()
        fctv_model = self.final_category_table_view.model()
        sctv_results = []
        # Select checked categories to the final category table
        # for row in range(row_count):
        row_count = sctv_model.rowCount()
        row = 0
        while True:
            checked = sctv_model.data(sctv_model.index(row, 0), Qt.CheckStateRole)
            item = sctv_model.data(sctv_model.index(row, 0))
            if checked == 2:
                sctv_results.append(item)
                sctv_model.removeRow(row)
            else:
                row += 1
            if row >= row_count:
                break

        print(sctv_results)

        # Checking for the presence of an element in the final table
        fctv_results = []
        for row in range(fctv_model.rowCount()):
            item = fctv_model.data(fctv_model.index(row, 0))
            fctv_results.append(item)

        for category in sctv_results:
            category_item = QStandardItem()
            category_item.setData(category, Qt.DisplayRole)
            category_item.setCheckable(True)
            # If the element is not in the final table, add it
            if category_item.data(Qt.DisplayRole) not in fctv_results:
                self.fin_cat_model.appendRow(category_item)

    def remove_category(self):
        fctv_model = self.source_category_table_view.model()
        sctv_model = self.final_category_table_view.model()
        sctv_results = []
        # Select checked categories to the final category table
        # for row in range(row_count):
        row_count = sctv_model.rowCount()
        row = 0
        while True:
            checked = sctv_model.data(sctv_model.index(row, 0), Qt.CheckStateRole)
            item = sctv_model.data(sctv_model.index(row, 0))
            if checked == 2:
                sctv_results.append(item)
                sctv_model.removeRow(row)
            else:
                row += 1
            if row >= row_count:
                break

        print(sctv_results)

        # Checking for the presence of an element in the final table
        fctv_results = []
        for row in range(fctv_model.rowCount()):
            item = fctv_model.data(fctv_model.index(row, 0))
            fctv_results.append(item)

        for category in sctv_results:
            category_item = QStandardItem()
            category_item.setData(category, Qt.DisplayRole)
            category_item.setCheckable(True)
            # If the element is not in the final table, add it
            if category_item.data(Qt.DisplayRole) not in fctv_results:
                self.source_cat_model.insertRow(0, category_item)

    # open xml file
    def open_file(self):
        file_path, _ = QFileDialog.getOpenFileName(filter="XML Files (*.xml)")
        categories = self.parse(file_path)
        self.populate_source_cat_table(categories)
        print("File closed")

    def populate_source_cat_table(self, categories):
        for category in categories:
            category_item = QStandardItem()
            category_item.setCheckable(True)
            category_item.setData(category, Qt.DisplayRole)
            self.source_cat_model.appendRow(category_item)

    @staticmethod
    def parse(file_path):
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

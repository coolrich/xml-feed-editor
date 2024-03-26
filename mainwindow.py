from PySide6.QtCore import QSortFilterProxyModel
from PySide6.QtCore import Qt
from PySide6.QtGui import QStandardItemModel, QStandardItem
from PySide6.QtWidgets import QMainWindow, QFileDialog, QTableView
from bs4 import BeautifulSoup

from ui_mainwindow import Ui_MainWindow


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, app):
        super().__init__()
        self.setupUi(self)
        self.app = app

        # Init of source_category_table_view
        category_header_name = ["Категорія"]
        self.source_cat_model = QStandardItemModel()
        self.source_cat_model.setHorizontalHeaderLabels(category_header_name)
        self.source_cat_proxy_model = QSortFilterProxyModel()
        self.source_cat_proxy_model.setSourceModel(self.source_cat_model)
        self.source_cat_proxy_model.setFilterKeyColumn(0)
        self.source_category_table_view.setModel(self.source_cat_proxy_model)
        self.source_category_table_view.resizeColumnsToContents()
        self.source_category_table_view.horizontalHeader().setStretchLastSection(True)
        self.source_category_table_view.horizontalHeader().setDefaultAlignment(Qt.AlignLeft)

        # Init of final_category_table_view
        self.fin_cat_model = QStandardItemModel()
        self.fin_cat_model.setHorizontalHeaderLabels(category_header_name)
        self.final_category_table_view.setModel(self.fin_cat_model)
        self.final_category_table_view.resizeColumnsToContents()
        self.final_category_table_view.horizontalHeader().setStretchLastSection(True)
        self.final_category_table_view.horizontalHeader().setDefaultAlignment(Qt.AlignLeft)

        # Init of products_table_view
        product_header_name = ["Товар", "Дроп Ціна", "Націнка", "Оптова Ціна", "Націнка"]
        self.products_model = QStandardItemModel()
        self.products_model.setHorizontalHeaderLabels(product_header_name)
        self.products_proxy_model = QSortFilterProxyModel()
        self.products_proxy_model.setSourceModel(self.products_model)
        self.products_proxy_model.setFilterKeyColumn(0)
        self.source_products_table_view.setModel(self.products_proxy_model)
        self.source_products_table_view.resizeColumnsToContents()
        self.source_products_table_view.horizontalHeader().setStretchLastSection(True)
        self.source_products_table_view.horizontalHeader().setDefaultAlignment(Qt.AlignLeft)

        self.search_category_line_edit.textChanged.connect(self.onTextChanged)
        self.open_action.triggered.connect(self.open_file)
        # self.add_cat_push_button.clicked.connect(self.add_category_into_table)
        self.add_cat_push_button.clicked.connect(
            lambda: self.move_items_between_tables(self.source_category_table_view, self.final_category_table_view))
        # self.delete_cat_push_button.clicked.connect(self.remove_category_from_table)
        self.delete_cat_push_button.clicked.connect(
            lambda: self.move_items_between_tables(self.final_category_table_view, self.source_category_table_view))
        self.fin_cat_model.rowsInserted.connect(self.add_products_to_table)
        self.fin_cat_model.rowsRemoved.connect(self.remove_products_from_table)
        self.xml_data = None

    def add_products_to_table(self):
        sptv_model = self.source_products_table_view.model()
        print("Data has been added to table")

    def remove_products_from_table(self):
        sptv_model = self.source_products_table_view.model()
        print("Data has been removed from table")

    def onTextChanged(self, text):
        self.source_cat_proxy_model.setFilterFixedString(text)

    from PySide6.QtCore import Qt

    @staticmethod
    def move_items_between_tables(source_table_view: QTableView,
                                  destination_table_view: QTableView):
        """
        Moves checked items from the source table view to the destination table view.

        Args:
            source_table_view (QtWidgets.QTableView): The source table view.
            destination_table_view (QtWidgets.QTableView): The destination table view.
        """

        # Get source and destination models
        source_model = source_table_view.model()
        destination_model = destination_table_view.model()

        if not source_model or not destination_model:
            print("Error: Invalid table view models.")
            return

        # Collect checked items in source model
        source_results = []
        row_count = source_model.rowCount()
        row = 0
        while row < row_count:
            checked = source_model.data(source_model.index(row, 0), Qt.CheckStateRole)
            if checked == 2:
                item = source_model.data(source_model.index(row, 0))
                source_results.append(item)
                source_model.removeRow(row)
            else:
                row += 1

        # Check for destination model existence (improved error handling)
        if not destination_model:
            print("Error: Destination table view has no model.")
            return

        # Collect existing items in destination model
        destination_results = []
        for row in range(destination_model.rowCount()):
            item = destination_model.data(destination_model.index(row, 0))
            destination_results.append(item)

        # Add unique items from source to destination
        for category in source_results:
            category_item = QStandardItem()
            category_item.setData(category, Qt.DisplayRole)
            category_item.setCheckable(True)
            if category_item.data(Qt.DisplayRole) not in destination_results:
                if destination_model.__class__ == QStandardItemModel:
                    destination_model.appendRow(category_item)
                    continue
                destination_model.sourceModel().appendRow(category_item)

        print("The process of moving items has been completed.")


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

import gc
import pprint

from PySide6.QtCore import QSortFilterProxyModel, QRegularExpression
from PySide6.QtCore import Qt
from PySide6.QtGui import QStandardItemModel, QStandardItem
from PySide6.QtWidgets import QMainWindow, QFileDialog, QTableView, QHeaderView, QItemDelegate
from lxml import etree

from ui_mainwindow import Ui_MainWindow


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, app):
        super().__init__()
        self.setupUi(self)
        self.app = app

        self.categories_products_dict = None

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
        self.source_category_table_view.setEditTriggers(QTableView.NoEditTriggers)

        # Init of final_category_table_view
        self.fin_cat_model = QStandardItemModel()
        self.fin_cat_model.setHorizontalHeaderLabels(category_header_name)
        self.fin_cat_proxy_model = QSortFilterProxyModel()
        self.fin_cat_proxy_model.setSourceModel(self.fin_cat_model)
        self.fin_cat_proxy_model.setFilterKeyColumn(0)
        self.final_category_table_view.setModel(self.fin_cat_proxy_model)
        self.final_category_table_view.resizeColumnsToContents()
        self.final_category_table_view.horizontalHeader().setStretchLastSection(True)
        self.final_category_table_view.horizontalHeader().setDefaultAlignment(Qt.AlignLeft)
        self.final_category_table_view.setEditTriggers(QTableView.NoEditTriggers)

        # Init of products_table_view
        product_header_name = ["Товар", "Дроп Ціна"]
        self.source_products_model = QStandardItemModel()
        self.source_products_model.setHorizontalHeaderLabels(product_header_name)
        self.source_products_proxy_model = QSortFilterProxyModel()
        self.source_products_proxy_model.setSourceModel(self.source_products_model)
        self.source_products_proxy_model.setFilterKeyColumn(0)
        self.source_products_table_view.setModel(self.source_products_proxy_model)
        self.source_products_table_view.resizeColumnsToContents()
        self.source_products_table_view.setEditTriggers(QTableView.NoEditTriggers)
        self.source_products_table_view.horizontalHeader().setDefaultAlignment(Qt.AlignLeft)
        self.source_products_table_view.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)

        class NoEditDelegate(QItemDelegate):
            def editorEvent(self, event, model, index, *args, **kwargs):
                # Дозволити редагування лише в 2-му та 4-му стовпчиках
                src_model = model.sourceModel()
                # Get index of the table from src_model
                # print(type(index.index))
                if index.column() not in (2, 4):
                    return super().editorEvent(event, model, index, *args, **kwargs)
                else:
                    return False

        fin_product_header_name = ["Товар", "Дроп Ціна", "Націнка", "Опт. Ціна", "Опт. Націнка"]
        self.fin_products_model = QStandardItemModel()
        self.fin_products_model.setHorizontalHeaderLabels(fin_product_header_name)
        self.fin_products_proxy_model = QSortFilterProxyModel()
        self.fin_products_proxy_model.setSourceModel(self.fin_products_model)
        self.fin_products_proxy_model.setFilterKeyColumn(0)
        self.final_products_table_view.setModel(self.fin_products_proxy_model)
        self.final_products_table_view.resizeColumnsToContents()
        # self.final_products_table_view.setEditTriggers(QTableView.NoEditTriggers)
        self.final_products_table_view.horizontalHeader().setDefaultAlignment(Qt.AlignLeft)
        # self.final_products_table_view.setItemDelegate(NoEditDelegate())

        self.search_src_category_line_edit.textChanged.connect(self.find_in_src_categories)
        self.search_fin_category_line_edit.textChanged.connect(self.find_in_fin_categories)
        self.search_src_product_line_edit.textChanged.connect(self.find_in_src_products)
        self.search_fin_product_line_edit.textChanged.connect(self.find_in_fin_products)
        self.open_action.triggered.connect(self.open_file)

        self.add_cat_push_button.clicked.connect(
            lambda: self.move_categories_between_tables(self.source_category_table_view,
                                                        self.final_category_table_view))
        # self.delete_cat_push_button.clicked.connect(self.remove_category_from_table)
        self.delete_cat_push_button.clicked.connect(
            lambda: self.move_categories_between_tables(self.final_category_table_view,
                                                        self.source_category_table_view))
        self.fin_cat_model.rowsInserted.connect(self.add_products_to_src_products_table)
        self.add_prod_push_button.clicked.connect(
            lambda: self.move_products_from_source_to_destination_table(
                self.source_products_table_view, self.final_products_table_view)
        )
        self.remove_prod_push_button.clicked.connect(
            lambda: self.move_products_from_source_to_destination_table(
                self.final_products_table_view, self.source_products_table_view)
        )
        self.fin_cat_model.rowsAboutToBeRemoved.connect(self.refresh_products_in_product_tables)
        self.apply_multiplier_push_button.clicked.connect(self.apply_multiplier)
        self.xml_data = None

    def apply_multiplier(self):


    def add_products_to_src_products_table(self):
        sptv_model = self.source_products_table_view.model()
        # Get all categories from self.final_category_table_view
        fin_cat_model = self.final_category_table_view.model()
        categories = set()
        for row in range(fin_cat_model.rowCount()):
            item = fin_cat_model.data(fin_cat_model.index(row, 0))
            categories.add(item)

        # Gather all products names from sptv_model in source_products_list
        source_products_set = set()
        for row in range(sptv_model.rowCount()):
            item = sptv_model.data(sptv_model.index(row, 0))
            source_products_set.add(item)

        for category in categories:
            products_list = self.categories_products_dict[category]
            for product_price_tuple in products_list:
                product_name = product_price_tuple[0]
                if product_name in source_products_set:
                    continue
                product_price = product_price_tuple[1]
                product_item = QStandardItem()
                product_item.setData(product_name, Qt.DisplayRole)
                product_item.setCheckable(True)
                price_item = QStandardItem()
                price_item.setData(product_price, Qt.DisplayRole)
                sptv_model.sourceModel().appendRow([product_item, price_item])
        self.source_products_table_view.resizeColumnsToContents()
        # self.source_products_table_view.horizontalHeader().setStretchLastSection(True)
        print("Data has been added to table")

    @staticmethod
    def move_products_from_source_to_destination_table(source_tabel, destination_tabel):
        source_model = source_tabel.model()
        destination_model = destination_tabel.model()

        if not source_model or not destination_model:
            print("Error: Invalid table view models.")
            return

        # Collect checked items in source model
        source_results = set()
        row_count = source_model.rowCount()
        row = 0
        while row < row_count:
            checked = source_model.data(source_model.index(row, 0), Qt.CheckStateRole)
            if checked == 2:
                # Collect all 5 columns of data
                data = []
                for col in range(source_model.columnCount()):
                    data.append(source_model.data(source_model.index(row, col)))
                source_results.add(tuple(data))
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
            # Collect all columns from destination model (assuming same structure)
            data = []
            for col in range(destination_model.columnCount()):
                data.append(destination_model.data(destination_model.index(row, col)))
            destination_results.append(data)
        # Add unique items from source to destination (considering all columns)
        for item_data in source_results:
            # Check if item already exists based on a unique identifier (e.g., "Товар")
            if item_data[0] not in [result[0] for result in destination_results]:
                new_item = []
                col_count = destination_model.columnCount()
                # for value in item_data:
                for col_num in range(col_count):
                    column_item = QStandardItem()
                    if col_num >= len(item_data):
                        column_item.setData(0, Qt.DisplayRole)
                    else:
                        column_item.setData(item_data[col_num], Qt.DisplayRole)
                    column_item.setCheckable(True if col_num == 0 else False)  # Set checkable only for the first column
                    if col_num == 3:
                        column_item.setEditable(True)
                    else:
                        column_item.setEditable(False)
                    new_item.append(column_item)

                if destination_model.__class__ == QStandardItemModel:
                    destination_model.appendRow(new_item)
                else:
                    destination_model.sourceModel().appendRow(new_item)
                print("Item", new_item, "has been removed")
        destination_tabel.resizeColumnToContents(0)
        source_tabel.resizeColumnToContents(0)
        print("The process of moving items has been completed.")

        print("Data has been added to table")

    def refresh_products_in_product_tables(self):
        sptv_model = self.source_products_table_view.model()
        fptv_model = self.final_products_table_view.model()
        sptv_model.removeRows(0, sptv_model.rowCount())
        fptv_model.removeRows(0, fptv_model.rowCount())
        self.add_products_to_src_products_table()
        self.move_products_from_source_to_destination_table(
            self.source_products_table_view,
            self.final_products_table_view
        )

        print("Data has been removed from table")

    def find_in_src_categories(self, text):
        self.source_cat_proxy_model.setFilterFixedString(text)
        self.source_cat_proxy_model.setFilterCaseSensitivity(Qt.CaseInsensitive)

    def find_in_fin_categories(self, text):
        self.fin_cat_proxy_model.setFilterFixedString(text)
        self.fin_cat_proxy_model.setFilterCaseSensitivity(Qt.CaseInsensitive)

    def find_in_src_products(self, text):
        self.source_products_table_view.model().setFilterFixedString(text)
        self.source_products_table_view.model().setFilterCaseSensitivity(Qt.CaseInsensitive)

    def find_in_fin_products(self, text):
        self.final_products_table_view.model().setFilterFixedString(text)
        self.final_products_table_view.model().setFilterCaseSensitivity(Qt.CaseInsensitive)

    def move_categories_between_tables(self, source_table_view: QTableView,
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
        if not categories:
            return
        self.categories_products_dict = categories
        self.reset_tables_data()
        self.populate_source_cat_table(categories)
        print("File closed")

    def reset_tables_data(self):
        self.source_cat_model.removeRows(0, self.source_cat_model.rowCount())
        self.fin_cat_model.removeRows(0, self.fin_cat_model.rowCount())

    def populate_source_cat_table(self, categories):
        for category in categories:
            category_item = QStandardItem()
            category_item.setCheckable(True)
            category_item.setData(category, Qt.DisplayRole)
            self.source_cat_model.appendRow(category_item)

    @staticmethod
    def parse(file_path):
        if not file_path:
            return None
        parser = etree.XMLParser(encoding="windows-1251")
        tree = etree.parse(file_path, parser=parser)
        category_elems = tree.xpath("//category")
        category_id_name_dict = {}

        categories = set()
        for category in category_elems:
            category_id = category.get("id").strip()
            category_name = category.text.strip()
            categories.add(category_name)
            category_id_name_dict[category_id] = category_name

        category_products_dict = {}
        for category in categories:
            category_products_dict[category] = []

        offer_tags = tree.xpath("//offer")
        for offer_tag in offer_tags:
            category_id = offer_tag.xpath("categoryId")
            product_name = offer_tag.xpath("name")[0].text.strip()
            product_price = offer_tag.xpath("price")[0].text.strip()
            product_price = int(product_price)
            cid = category_id[0].text.strip()
            print(cid)
            if cid not in category_id_name_dict:
                continue
            category_name = category_id_name_dict[cid]
            category_products_dict[category_name].append((product_name, product_price))
        pprint.pp(category_products_dict)

        # del tree, categories, offer_tags
        gc.collect()
        return category_products_dict

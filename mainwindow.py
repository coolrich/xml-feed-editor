import copy
import gc
import pprint
import re

from PySide6.QtCore import QSortFilterProxyModel
from PySide6.QtCore import Qt
from PySide6.QtGui import QStandardItemModel, QStandardItem
from PySide6.QtWidgets import QMainWindow, QFileDialog, QTableView, QHeaderView, QItemDelegate, QMessageBox
from lxml import etree
from lxml.etree import ElementTree

from ui_mainwindow import Ui_MainWindow


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, app):
        super().__init__()
        self.setupUi(self)
        self.app = app
        self.setWindowTitle("XML parser")

        self.categoryid_name_dict = None
        self.all_categories_products_dict = None
        self.chosed_categories_products_dict = None
        self.source_xml_tree = None
        self.final_xml_tree = None

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
        product_header_name = ["Товар", "Початкова Ціна"]
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

        fin_product_header_name = ["Товар", "Початкова Ціна", "Оптова Ціна", "Дроп Ціна"]
        self.fin_products_model = QStandardItemModel()
        self.fin_products_model.setHorizontalHeaderLabels(fin_product_header_name)
        self.fin_products_proxy_model = QSortFilterProxyModel()
        self.fin_products_proxy_model.setSourceModel(self.fin_products_model)
        self.fin_products_proxy_model.setFilterKeyColumn(0)
        self.final_products_table_view.setModel(self.fin_products_proxy_model)
        self.final_products_table_view.resizeColumnsToContents()
        self.final_products_table_view.horizontalHeader().setDefaultAlignment(Qt.AlignLeft)

        self.search_src_category_line_edit.textChanged.connect(self.find_in_src_categories)
        self.search_fin_category_line_edit.textChanged.connect(self.find_in_fin_categories)
        self.search_src_product_line_edit.textChanged.connect(self.find_in_src_products)
        self.search_fin_product_line_edit.textChanged.connect(self.find_in_fin_products)
        self.open_action.triggered.connect(self.open_file)

        self.add_cat_push_button.clicked.connect(
            lambda: self.move_categories_between_tables(self.source_category_table_view,
                                                        self.final_category_table_view))
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
        self.get_new_xml_push_button.clicked.connect(self.get_new_xml)
        self.bottom_price_limit_spin_box.valueChanged.connect(self.checkForBottomPriceValue)
        self.upper_price_limit_spin_box.valueChanged.connect(self.checkForUpperPriceValu)
        # self.
        self.xml_data = None

    def checkForBottomPriceValue(self, value):
        if value > self.upper_price_limit_spin_box.value():
            self.bottom_price_limit_spin_box.setValue(self.bottom_price_limit_spin_box.value() - 1)
            # Show a warning window with message Нижня межа не може перевищувати верхню
            QMessageBox.warning(self, "Попередження",
                                "Нижня межа не може перевищувати верхню",
                                QMessageBox.Ok)

    def checkForUpperPriceValu(self, value):
        if value < self.bottom_price_limit_spin_box.value():
            self.upper_price_limit_spin_box.setValue(self.upper_price_limit_spin_box.value() + 1)
            QMessageBox.warning(self, "Попередження",
                                "Верхня межа не може бути менше за нижню!",
                                QMessageBox.Ok)

    def get_new_xml(self):
        final_category_model = self.final_category_table_view.model().sourceModel()
        final_prod_model = self.final_products_table_view.model().sourceModel()

        chosen_categories_list = []
        for row in range(final_category_model.rowCount()):
            chosed_products = final_category_model.data(final_category_model.index(row, 0))
            chosen_categories_list.append(chosed_products)

        chosen_products_dict = {}
        for row in range(final_prod_model.rowCount()):
            chosen_prod_name = final_prod_model.data(final_prod_model.index(row, 0))
            wholesale_price = final_prod_model.data(final_prod_model.index(row, 2))
            drop_price = final_prod_model.data(final_prod_model.index(row, 3))
            chosen_products_dict[chosen_prod_name] = {}
            if wholesale_price != 0:
                chosen_products_dict[chosen_prod_name]["wholesale_price"] = wholesale_price
            if drop_price != 0:
                chosen_products_dict[chosen_prod_name]["drop_price"] = drop_price

        # Create a copy of self.source_xml_tree
        self.final_xml_tree: ElementTree = copy.deepcopy(self.source_xml_tree)
        output_xml_tree = self.final_xml_tree
        if output_xml_tree is None:
            return

        # Remove unselected categories
        categories = output_xml_tree.xpath("//category")
        for category in categories:
            category_name = category.text.strip()
            if category_name not in chosen_categories_list:
                category.getparent().remove(category)

        # Remove products of unselected categories
        offers = output_xml_tree.xpath("//offer")
        categories_id_list = self.categoryid_name_dict.keys()
        for offer in offers:
            category_id = offer.xpath("categoryId")[0].text.strip()
            if category_id not in categories_id_list:
                offer.getparent().remove(offer)
                continue
            category_name = self.categoryid_name_dict[category_id]
            if category_name not in chosen_categories_list:
                offer.getparent().remove(offer)
                continue

        # Remove unselected products
        offers = output_xml_tree.xpath("//offer")
        for offer in offers:
            product_name = offer.xpath("name")[0].text.strip()
            if product_name not in chosen_products_dict.keys():
                offer.getparent().remove(offer)
            else:
                # Change price to new
                price = None
                if "wholesale_price" in chosen_products_dict[product_name].keys():
                    wholesale_price = chosen_products_dict[product_name]["wholesale_price"]
                    price = offer.xpath("price")[0]
                    price.text = str(wholesale_price)

                if price is not None and "drop_price" in chosen_products_dict[product_name].keys():
                    drop_price = chosen_products_dict[product_name]["drop_price"]
                    price_drop = etree.Element("price_drop")
                    price_drop.text = str(drop_price)
                    price.addnext(price_drop)

        # Create a window for saving a new xml file
        save_dialog = QFileDialog()
        save_dialog.setFileMode(QFileDialog.AnyFile)
        save_dialog.setAcceptMode(QFileDialog.AcceptSave)
        save_dialog.setNameFilter("XML Files (*.xml)")
        if save_dialog.exec_():
            save_path = save_dialog.selectedFiles()[0]
            self.final_xml_tree.write(save_path, encoding='windows-1251')
            self.change_encoding_letter_case_in_output_xml(save_path)
            self.correction_of_the_xml_elements(save_path)
            print(f"XML {save_path} created")
            return

    @staticmethod
    def correction_of_the_xml_elements(filename: str):
        with open(filename, "r") as f:
            text = f.read()
        pattern = r"</price_drop>"
        new_text = r"</price_drop>\n"
        new_content = re.sub(rf"{pattern}", new_text, text, flags=re.MULTILINE)
        with open(filename, "w") as f:
            f.write(new_content)

    @staticmethod
    def change_encoding_letter_case_in_output_xml(filename: str):
        with open(filename, "r") as f:
            text = f.read()
        text = text.replace(r"'WINDOWS-1251'", r'"windows-1251"')
        with open(filename, "w") as f:
            f.write(text)

    def apply_multiplier(self):
        """ Get value from price_category_combo_box
         Get value from bottom_price_limit_spin_box
         Get value from upper_price_limit_spin_box
         Get value from multiplier_double_spin_box
         Save them in variables
         Find all products in the final_products_table_view
         by column using valu from price_category_combo_box
         then filter them by range from bottom_price_limit_spin_box
         to upper_price_limit_spin_box. Save found products in resulted_products_list.
         Then apply value from multiplier_double_spin_box to each product price and save them in the next column.
         Then save and back products and their prices to final_products_table_view.
         """
        price_category = self.price_category_combo_box.currentText()
        bottom_price_limit = self.bottom_price_limit_spin_box.value()
        upper_price_limit = self.upper_price_limit_spin_box.value()
        multiplier = self.multiplier_double_spin_box.value()
        resulted_products_list = []

        # Get all products from self.final_products_table_view model
        fptv_tabel = self.final_products_table_view
        fptv_model: QStandardItemModel = fptv_tabel.model().sourceModel()
        column_index_target_price = None
        column_count = fptv_model.columnCount()
        for row_index in range(column_count):
            column_index_target_price = fptv_model.horizontalHeaderItem(row_index)
            if column_index_target_price.text() == price_category:
                column_index_target_price = row_index
                break
        # print(index)
        row_count = fptv_model.rowCount()
        for row in range(row_count):
            source_price = fptv_model.data(fptv_model.index(row, 1))
            final_price = fptv_model.data(fptv_model.index(row, column_index_target_price))
            if bottom_price_limit <= source_price <= upper_price_limit:
                product_markup = multiplier * source_price
                fptv_model.setData(fptv_model.index(row, column_index_target_price), product_markup)
            print(source_price)

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
            products_list = self.all_categories_products_dict[category]
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
        categories_products_dict = self.parse(file_path)
        if not categories_products_dict:
            return
        self.all_categories_products_dict = categories_products_dict
        self.reset_tables_data()
        self.populate_source_cat_table(categories_products_dict)
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

    def parse(self, file_path):
        if not file_path:
            return None
        parser = etree.XMLParser(encoding="windows-1251")
        self.source_xml_tree = etree.parse(file_path, parser=parser)
        category_elems = self.source_xml_tree.xpath("//category")
        categoryid_name_dict = {}

        categories = set()
        for category in category_elems:
            category_id = category.get("id").strip()
            category_name = category.text.strip()
            categories.add(category_name)
            categoryid_name_dict[category_id] = category_name
        self.categoryid_name_dict = categoryid_name_dict

        category_products_dict = {}
        for category in categories:
            category_products_dict[category] = []

        offer_tags = self.source_xml_tree.xpath("//offer")
        for offer_tag in offer_tags:
            category_id = offer_tag.xpath("categoryId")
            product_name = offer_tag.xpath("name")[0].text.strip()
            product_price = offer_tag.xpath("price")[0].text.strip()
            product_price = int(product_price)
            cid = category_id[0].text.strip()
            print(cid)
            if cid not in categoryid_name_dict:
                continue
            category_name = categoryid_name_dict[cid]
            category_products_dict[category_name].append((product_name, product_price))
        pprint.pp(category_products_dict)

        # del tree, categories, offer_tags
        gc.collect()
        return category_products_dict

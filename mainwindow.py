import copy
import gc
import pprint
import re

from PySide6.QtCore import QSortFilterProxyModel
from PySide6.QtCore import Qt
from PySide6.QtGui import QStandardItemModel, QStandardItem
from PySide6.QtWidgets import QMainWindow, QFileDialog, QTableView, QHeaderView, QMessageBox
from lxml import etree
from lxml.etree import ElementTree

from ui_mainwindow import Ui_MainWindow


class MainWindow(QMainWindow, Ui_MainWindow):
    DEFAULT_CATEGORY = "Без категорії"

    def __init__(self, app):
        super().__init__()
        self.setupUi(self)
        self.app = app
        self.setWindowTitle("XML parser")

        self.categoryid_name_dict = None
        self.all_categories_products_dict = None
        self.chosed_categories_products_dict = None
        self.input_xml_tree = None
        self.output_xml_tree = None

        # Init of input_category_table_view
        category_header_name = ["Категорія"]
        self.input_category_model = QStandardItemModel()
        self.input_category_model.setHorizontalHeaderLabels(category_header_name)
        self.input_category_proxy_model = QSortFilterProxyModel()
        self.input_category_proxy_model.setSourceModel(self.input_category_model)
        self.input_category_proxy_model.setFilterKeyColumn(0)
        self.input_category_table_view.setModel(self.input_category_proxy_model)
        self.input_category_table_view.resizeColumnsToContents()
        self.input_category_table_view.horizontalHeader().setStretchLastSection(True)
        self.input_category_table_view.horizontalHeader().setDefaultAlignment(Qt.AlignLeft)
        # noinspection PyUnresolvedReferences
        self.input_category_table_view.setEditTriggers(QTableView.NoEditTriggers)

        # Init of output_category_table_view
        self.output_category_model = QStandardItemModel()
        self.output_category_model.setHorizontalHeaderLabels(category_header_name)
        self.output_category_proxy_model = QSortFilterProxyModel()
        self.output_category_proxy_model.setSourceModel(self.output_category_model)
        self.output_category_proxy_model.setFilterKeyColumn(0)
        self.output_category_table_view.setModel(self.output_category_proxy_model)
        self.output_category_table_view.resizeColumnsToContents()
        self.output_category_table_view.horizontalHeader().setStretchLastSection(True)
        self.output_category_table_view.horizontalHeader().setDefaultAlignment(Qt.AlignLeft)
        # noinspection PyUnresolvedReferences
        self.output_category_table_view.setEditTriggers(QTableView.NoEditTriggers)

        # Init of products_table_view
        product_header_name = ["Товар", "Початкова Ціна"]
        self.input_products_model = QStandardItemModel()
        self.input_products_model.setHorizontalHeaderLabels(product_header_name)
        self.input_products_proxy_model = QSortFilterProxyModel()
        self.input_products_proxy_model.setSourceModel(self.input_products_model)
        self.input_products_proxy_model.setFilterKeyColumn(0)
        self.input_products_table_view.setModel(self.input_products_proxy_model)
        self.input_products_table_view.resizeColumnsToContents()
        # noinspection PyUnresolvedReferences
        self.input_products_table_view.setEditTriggers(QTableView.NoEditTriggers)
        self.input_products_table_view.horizontalHeader().setDefaultAlignment(Qt.AlignLeft)
        # noinspection PyUnresolvedReferences
        self.input_products_table_view.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)

        output_product_header_name = ["Товар", "Початкова Ціна", "Оптова Ціна", "Дроп Ціна"]
        self.output_products_model = QStandardItemModel()
        self.output_products_model.setHorizontalHeaderLabels(output_product_header_name)
        self.output_products_proxy_model = QSortFilterProxyModel()
        self.output_products_proxy_model.setSourceModel(self.output_products_model)
        self.output_products_proxy_model.setFilterKeyColumn(0)
        self.output_products_table_view.setModel(self.output_products_proxy_model)
        self.output_products_table_view.resizeColumnsToContents()
        self.output_products_table_view.horizontalHeader().setDefaultAlignment(Qt.AlignLeft)

        # Init of input_category_names_table_view
        input_category_header_name = ["Категорія"]
        self.input_category_names_model = QStandardItemModel()
        self.input_category_names_model.setHorizontalHeaderLabels(input_category_header_name)
        self.input_category_names_proxy_model = QSortFilterProxyModel()
        self.input_category_names_proxy_model.setSourceModel(self.input_category_names_model)
        self.input_category_names_proxy_model.setFilterKeyColumn(0)
        self.input_category_names_table_view.setModel(self.input_category_names_proxy_model)
        self.input_category_names_table_view.resizeColumnsToContents()
        self.input_category_names_table_view.horizontalHeader().setStretchLastSection(True)
        self.input_category_names_table_view.horizontalHeader().setDefaultAlignment(Qt.AlignLeft)
        # noinspection PyUnresolvedReferences
        self.input_category_names_table_view.setEditTriggers(QTableView.NoEditTriggers)

        # Init of search output_category_names_table_view
        output_category_header_name = ["Початкова назва", "Нова назва"]
        self.output_category_names_model = QStandardItemModel()
        self.output_category_names_model.setHorizontalHeaderLabels(output_category_header_name)
        self.output_category_names_proxy_model = QSortFilterProxyModel()
        self.output_category_names_proxy_model.setSourceModel(self.output_category_names_model)
        self.output_category_names_proxy_model.setFilterKeyColumn(0)
        self.output_category_names_table_view.setModel(self.output_category_names_proxy_model)
        self.output_category_names_table_view.resizeColumnsToContents()
        self.output_category_names_table_view.horizontalHeader().setDefaultAlignment(Qt.AlignLeft)

        # Init of input_category_names_table_view
        input_product_header_name = ["Товар"]
        self.input_product_names_model = QStandardItemModel()
        self.input_product_names_model.setHorizontalHeaderLabels(input_product_header_name)
        self.input_product_names_proxy_model = QSortFilterProxyModel()
        self.input_product_names_proxy_model.setSourceModel(self.input_product_names_model)
        self.input_product_names_proxy_model.setFilterKeyColumn(0)
        self.input_product_names_table_view.setModel(self.input_product_names_proxy_model)
        self.input_product_names_table_view.resizeColumnsToContents()
        self.input_product_names_table_view.horizontalHeader().setStretchLastSection(True)
        self.input_product_names_table_view.horizontalHeader().setDefaultAlignment(Qt.AlignLeft)

        # Init of search output_category_names_table_view
        output_product_header_name = ["Початкова назва", "Нова назва"]
        self.output_product_names_model = QStandardItemModel()
        self.output_product_names_model.setHorizontalHeaderLabels(output_product_header_name)
        self.output_product_proxy_model = QSortFilterProxyModel()
        self.output_product_proxy_model.setSourceModel(self.output_product_names_model)
        self.output_product_proxy_model.setFilterKeyColumn(0)
        self.output_product_names_table_view.setModel(self.output_product_proxy_model)
        self.output_product_names_table_view.resizeColumnsToContents()
        self.output_product_names_table_view.horizontalHeader().setDefaultAlignment(Qt.AlignLeft)

        self.search_input_category_line_edit.textChanged.connect(self.find_in_input_categories)
        self.search_output_category_line_edit.textChanged.connect(self.find_in_output_categories)
        self.search_input_product_line_edit.textChanged.connect(self.find_in_input_products)
        self.search_output_product_line_edit.textChanged.connect(self.find_in_output_products)
        self.open_action.triggered.connect(self.open_file)

        self.add_category_push_button.clicked.connect(
            lambda: self.move_categories_between_tables(self.input_category_table_view,
                                                        self.output_category_table_view))
        self.delete_category_push_button.clicked.connect(
            lambda: self.move_categories_between_tables(self.output_category_table_view,
                                                        self.input_category_table_view))
        self.output_category_model.rowsInserted.connect(self.add_products_to_src_products_table)
        self.add_product_push_button.clicked.connect(
            lambda: self.move_products_from_input_to_destination_table(
                self.input_products_table_view, self.output_products_table_view)
        )
        self.remove_product_push_button.clicked.connect(
            lambda: self.move_products_from_input_to_destination_table(
                self.output_products_table_view, self.input_products_table_view)
        )
        self.output_category_model.rowsAboutToBeRemoved.connect(self.refresh_products_in_product_tables)
        self.apply_multiplier_push_button.clicked.connect(self.apply_multiplier)
        self.get_new_xml_push_button.clicked.connect(self.get_new_xml)
        self.bottom_price_limit_spin_box.valueChanged.connect(self.checkForBottomPriceValue)
        self.upper_price_limit_spin_box.valueChanged.connect(self.checkForUpperPriceValu)
        self.action_about_qt.triggered.connect(self.about_qt)

        self.search_category_for_replace_line_edit.textChanged.connect(self.find_category_names_for_replace)
        self.replace_category_name_line_edit.textChanged.connect(self.replace_category_name_line_edit_text_change)
        self.replace_category_name_push_button.clicked.connect(self.replace_input_category_names)
        self.replace_category_name_push_button.setEnabled(False)

        self.search_product_for_replace_line_edit.textChanged.connect(self.find_product_names_for_replace)
        self.replace_product_name_line_edit.textChanged.connect(self.replace_product_name_line_edit_text_change)
        self.replace_product_name_push_button.clicked.connect(self.replace_input_product_names)
        self.replace_product_name_push_button.setEnabled(False)

        self.xml_data = None

    def find_category_names_for_replace(self, text):
        # TODO: Does it need to be case-insensitive?
        # self.input_category_names_proxy_model.setFilterCaseSensitivity(Qt.CaseInsensitive)
        self.input_category_names_proxy_model.setFilterRegularExpression(text)
        input_category_names_count = self.input_category_names_proxy_model.rowCount()
        if (input_category_names_count == 0
                or text == ""
                or self.replace_category_name_line_edit.text() == ""):
            self.replace_category_name_push_button.setEnabled(False)
        else:
            self.replace_category_name_push_button.setEnabled(True)

    def find_product_names_for_replace(self, text):
        # TODO: Does it need to be case-insensitive?
        # self.input_product_names_proxy_model.setFilterCaseSensitivity(Qt.CaseInsensitive)
        self.input_product_names_proxy_model.setFilterRegularExpression(text)
        input_product_names_count = self.input_product_names_proxy_model.rowCount()
        if (input_product_names_count == 0
                or text == ""
                or self.replace_product_name_line_edit.text() == ""):
            self.replace_product_name_push_button.setEnabled(False)
        else:
            self.replace_product_name_push_button.setEnabled(True)

    def replace_category_name_line_edit_text_change(self, text):
        if (self.input_category_names_proxy_model.rowCount() == 0
                or text == ""
                or self.replace_category_name_line_edit.text() == ""):
            self.replace_category_name_push_button.setEnabled(False)
        else:
            self.replace_category_name_push_button.setEnabled(True)

    def replace_product_name_line_edit_text_change(self, text):
        if (self.input_product_names_proxy_model.rowCount() == 0
                or text == ""
                or self.replace_product_name_line_edit.text() == ""):
            self.replace_product_name_push_button.setEnabled(False)
        else:
            self.replace_product_name_push_button.setEnabled(True)

    def replace_input_category_names(self):
        rows_count = self.input_category_names_proxy_model.rowCount()
        for row in range(rows_count):
            item = self.input_category_names_proxy_model.data(self.input_category_names_proxy_model.index(row, 0),
                                                              Qt.DisplayRole)
            print(item)

    def replace_input_product_names(self):
        rows_count = self.input_product_names_proxy_model.rowCount()
        for row in range(rows_count):
            item = self.input_product_names_proxy_model.data(self.input_product_names_proxy_model.index(row, 0),
                                                             Qt.DisplayRole)
            print(item)

    def find_in_input_categories(self, text):
        self.input_category_proxy_model.setFilterCaseSensitivity(Qt.CaseInsensitive)
        self.input_category_proxy_model.setFilterRegularExpression(text)

    def find_in_output_categories(self, text):
        self.output_category_proxy_model.setFilterCaseSensitivity(Qt.CaseInsensitive)
        self.output_category_proxy_model.setFilterFixedString(text)

    def find_in_input_products(self, text):
        self.input_products_table_view.model().setFilterFixedString(text)
        self.input_products_table_view.model().setFilterCaseSensitivity(Qt.CaseInsensitive)

    def find_in_output_products(self, text):
        self.output_products_table_view.model().setFilterFixedString(text)
        self.output_products_table_view.model().setFilterCaseSensitivity(Qt.CaseInsensitive)

    def about_qt(self):
        QMessageBox.aboutQt(self)

    def checkForBottomPriceValue(self, value):
        if value > self.upper_price_limit_spin_box.value():
            self.bottom_price_limit_spin_box.setValue(self.bottom_price_limit_spin_box.value() - 1)
            # Show a warning window with message Нижня межа не може перевищувати верхню
            # noinspection PyUnresolvedReferences
            QMessageBox.warning(self, "Попередження",
                                "Нижня межа не може перевищувати верхню",
                                QMessageBox.Ok)

    def checkForUpperPriceValu(self, value):
        if value < self.bottom_price_limit_spin_box.value():
            self.upper_price_limit_spin_box.setValue(self.upper_price_limit_spin_box.value() + 1)
            # noinspection PyUnresolvedReferences
            QMessageBox.warning(self, "Попередження",
                                "Верхня межа не може бути менше за нижню!",
                                QMessageBox.Ok)

    def get_new_xml(self):
        final_category_model = self.output_category_table_view.model().sourceModel()
        final_prod_model = self.output_products_table_view.model().sourceModel()

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

        # Create a copy of self.input_xml_tree
        self.output_xml_tree: ElementTree = copy.deepcopy(self.input_xml_tree)
        output_xml_tree = self.output_xml_tree
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
            if category_id in categories_id_list:
                category_name = self.categoryid_name_dict[category_id]
            else:
                category_name = MainWindow.DEFAULT_CATEGORY

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
        # noinspection PyUnresolvedReferences
        save_dialog.setFileMode(QFileDialog.AnyFile)
        # noinspection PyUnresolvedReferences
        save_dialog.setAcceptMode(QFileDialog.AcceptSave)
        save_dialog.setNameFilter("XML Files (*.xml)")
        if save_dialog.exec_():
            save_path = save_dialog.selectedFiles()[0]
            self.output_xml_tree.write(save_path, encoding='windows-1251')
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
         Find all products in the output_products_table_view
         by column using valu from price_category_combo_box
         then filter them by range from bottom_price_limit_spin_box
         to upper_price_limit_spin_box. Save found products in resulted_products_list.
         Then apply value from multiplier_double_spin_box to each product price and save them in the next column.
         Then save and back products and their prices to output_products_table_view.
         """
        price_category = self.price_category_combo_box.currentText()
        bottom_price_limit = self.bottom_price_limit_spin_box.value()
        upper_price_limit = self.upper_price_limit_spin_box.value()
        multiplier = self.multiplier_double_spin_box.value()
        resulted_products_list = []

        # Get all products from self.output_products_table_view model
        fptv_tabel = self.output_products_table_view
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
            input_price = fptv_model.data(fptv_model.index(row, 1))
            final_price = fptv_model.data(fptv_model.index(row, column_index_target_price))
            if bottom_price_limit <= input_price <= upper_price_limit:
                product_markup = multiplier * input_price
                fptv_model.setData(fptv_model.index(row, column_index_target_price), product_markup)
            print(input_price)

    def add_products_to_src_products_table(self):
        sptv_model = self.input_products_table_view.model()
        # Get all categories from self.output_category_table_view
        output_category_model = self.output_category_table_view.model()
        categories = set()
        for row in range(output_category_model.rowCount()):
            item = output_category_model.data(output_category_model.index(row, 0))
            categories.add(item)

        # Gather all products names from sptv_model in input_products_list
        input_products_set = set()
        for row in range(sptv_model.rowCount()):
            item = sptv_model.data(sptv_model.index(row, 0))
            input_products_set.add(item)

        for category in categories:
            products_list = self.all_categories_products_dict[category]
            for product_price_tuple in products_list:
                product_name = product_price_tuple[0]
                if product_name in input_products_set:
                    continue
                product_price = product_price_tuple[1]
                product_item = QStandardItem()
                product_item.setData(product_name, Qt.DisplayRole)
                product_item.setCheckable(True)
                price_item = QStandardItem()
                price_item.setData(product_price, Qt.DisplayRole)
                sptv_model.sourceModel().appendRow([product_item, price_item])
        self.input_products_table_view.resizeColumnsToContents()
        # self.input_products_table_view.horizontalHeader().setStretchLastSection(True)
        print("Data has been added to table")

    @staticmethod
    def move_products_from_input_to_destination_table(input_tabel, destination_tabel):
        input_model = input_tabel.model()
        destination_model = destination_tabel.model()

        if not input_model or not destination_model:
            print("Error: Invalid table view models.")
            return

        # Collect checked items in source model
        input_results = set()
        row_count = input_model.rowCount()
        row = 0
        while row < row_count:
            checked = input_model.data(input_model.index(row, 0), Qt.CheckStateRole)
            if checked == 2:
                # Collect all 5 columns of data
                data = []
                for col in range(input_model.columnCount()):
                    data.append(input_model.data(input_model.index(row, col)))
                input_results.add(tuple(data))
                input_model.removeRow(row)
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
        for item_data in input_results:
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
        input_tabel.resizeColumnToContents(0)
        print("The process of moving items has been completed.")
        print("Data has been added to table")

    def refresh_products_in_product_tables(self):
        sptv_model = self.input_products_table_view.model()
        fptv_model = self.output_products_table_view.model()
        sptv_model.removeRows(0, sptv_model.rowCount())
        fptv_model.removeRows(0, fptv_model.rowCount())
        self.add_products_to_src_products_table()
        self.move_products_from_input_to_destination_table(
            self.input_products_table_view,
            self.output_products_table_view
        )

        print("Data has been removed from table")

    @staticmethod
    def move_categories_between_tables(input_table_view: QTableView,
                                       destination_table_view: QTableView):
        """
        Moves checked items from the source table view to the destination table view.

        Args:
            input_table_view (QtWidgets.QTableView): The source table view.
            destination_table_view (QtWidgets.QTableView): The destination table view.
        """
        # Get source and destination models
        input_model = input_table_view.model()
        destination_model = destination_table_view.model()

        if not input_model or not destination_model:
            print("Error: Invalid table view models.")
            return

        # Collect checked items in source model
        input_results = []
        row_count = input_model.rowCount()
        row = 0
        while row < row_count:
            checked = input_model.data(input_model.index(row, 0), Qt.CheckStateRole)
            if checked == 2:
                item = input_model.data(input_model.index(row, 0))
                input_results.append(item)
                input_model.removeRow(row)
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
        for category in input_results:
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
        self.populate_input_tables(categories_products_dict)
        print("File closed")

    def reset_tables_data(self):
        self.input_category_model.removeRows(0, self.input_category_model.rowCount())
        self.output_category_model.removeRows(0, self.output_category_model.rowCount())

    def populate_input_tables(self, categories):
        for category in categories:
            category_item = QStandardItem()
            category_item.setCheckable(True)
            category_item.setData(category, Qt.DisplayRole)
            self.input_category_model.appendRow(category_item)

            category_name_item = QStandardItem()
            category_name_item.setData(category, Qt.DisplayRole)
            self.input_category_names_model.appendRow(category_name_item)

        all_products_list = []
        for product_names_list in self.all_categories_products_dict.values():
            all_products_list.extend(product_names_list)

        for product_name in all_products_list:
            product_name_item = QStandardItem()
            product_name_item.setData(product_name[0], Qt.DisplayRole)
            self.input_product_names_model.appendRow(product_name_item)

    def parse(self, file_path):
        if not file_path:
            return None
        parser = etree.XMLParser(encoding="windows-1251")
        self.input_xml_tree = etree.parse(file_path, parser=parser)
        category_elems = self.input_xml_tree.xpath("//category")
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

        # Add the category MainWindow.DEFAULT_CATEGORY for products without category
        category_products_dict[MainWindow.DEFAULT_CATEGORY] = []

        offer_tags = self.input_xml_tree.xpath("//offer")
        for offer_tag in offer_tags:
            category_id = offer_tag.xpath("categoryId")
            product_name = offer_tag.xpath("name")[0].text.strip()
            product_price = offer_tag.xpath("price")[0].text.strip()
            product_price = int(product_price)
            cid = category_id[0].text.strip()
            print(cid)
            if cid not in categoryid_name_dict:
                # Add product to the category MainWindow.DEFAULT_CATEGORY
                category_products_dict[MainWindow.DEFAULT_CATEGORY].append((product_name, product_price))
                continue
            category_name = categoryid_name_dict[cid]
            category_products_dict[category_name].append((product_name, product_price))
        pprint.pp(category_products_dict)

        # del tree, categories, offer_tags
        gc.collect()
        return category_products_dict

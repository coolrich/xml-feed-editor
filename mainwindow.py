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
    DEFAULT_CATEGORY_NAME = "Без категорії"
    DEFAULT_CATEGORY_ID = "-1"

    def __init__(self, app):
        super().__init__()
        self.setupUi(self)
        self.app = app
        self.setWindowTitle("XML parser")

        self.categoryid_name_dict: dict[str, str] = {}
        # key:cid value: [{"product_id": product_id, "product_name": product_name, "product_price": product_price}]
        self.all_category_ids_products_dict: dict[str, list[dict[str:str, str:str, str:int]]] = {}
        self.chosed_categories_products_dict = None
        self.input_xml_tree = None
        self.output_xml_tree = None

        # Init of input_category_table_view
        category_header_name = ["Категорія", "ID"]
        self.input_category_model = QStandardItemModel()
        self.input_category_model.setHorizontalHeaderLabels(category_header_name)
        self.input_category_proxy_model = QSortFilterProxyModel()
        self.input_category_proxy_model.setSourceModel(self.input_category_model)
        self.input_category_proxy_model.setFilterKeyColumn(0)
        self.input_category_table_view.setModel(self.input_category_proxy_model)
        self.input_category_table_view.resizeColumnsToContents()
        # self.input_category_table_view.horizontalHeader().setStretchLastSection(True)
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
        # self.output_category_table_view.horizontalHeader().setStretchLastSection(True)
        self.output_category_table_view.horizontalHeader().setDefaultAlignment(Qt.AlignLeft)
        # noinspection PyUnresolvedReferences
        self.output_category_table_view.setEditTriggers(QTableView.NoEditTriggers)

        # Init of products_table_view
        product_header_name = ["Товар", "Початкова Ціна", "ID"]
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

        output_product_header_name = ["Товар", "Початкова Ціна", "Оптова Ціна", "Дроп Ціна", "ID"]
        self.output_products_model = QStandardItemModel()
        self.output_products_model.setHorizontalHeaderLabels(output_product_header_name)
        self.output_products_proxy_model = QSortFilterProxyModel()
        self.output_products_proxy_model.setSourceModel(self.output_products_model)
        self.output_products_proxy_model.setFilterKeyColumn(0)
        self.output_products_table_view.setModel(self.output_products_proxy_model)
        self.output_products_table_view.resizeColumnsToContents()
        self.output_products_table_view.horizontalHeader().setDefaultAlignment(Qt.AlignLeft)

        # Init of input_category_names_table_view
        input_category_header_name = ["Категорія", "ID"]
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
        output_category_header_name = ["Початкова назва", "Нова назва", "ID"]
        self.output_category_names_model = QStandardItemModel()
        self.output_category_names_model.setHorizontalHeaderLabels(output_category_header_name)
        self.output_category_names_proxy_model = QSortFilterProxyModel()
        self.output_category_names_proxy_model.setSourceModel(self.output_category_names_model)
        self.output_category_names_proxy_model.setFilterKeyColumn(0)
        self.output_category_names_table_view.setModel(self.output_category_names_proxy_model)
        self.output_category_names_table_view.resizeColumnsToContents()
        self.output_category_names_table_view.horizontalHeader().setDefaultAlignment(Qt.AlignLeft)

        # Init of input_category_names_table_view
        input_product_header_name = ["Товар", "ID"]
        self.input_product_names_model = QStandardItemModel()
        self.input_product_names_model.setHorizontalHeaderLabels(input_product_header_name)
        self.input_product_proxy_model = QSortFilterProxyModel()
        self.input_product_proxy_model.setSourceModel(self.input_product_names_model)
        self.input_product_proxy_model.setFilterKeyColumn(0)
        self.input_product_names_table_view.setModel(self.input_product_proxy_model)
        self.input_product_names_table_view.resizeColumnsToContents()
        self.input_product_names_table_view.horizontalHeader().setStretchLastSection(True)
        self.input_product_names_table_view.horizontalHeader().setDefaultAlignment(Qt.AlignLeft)

        # Init of search output_category_names_table_view
        output_product_header_name = ["Початкова назва", "Нова назва", "ID"]
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
        self.replace_category_name_push_button.setEnabled(False)
        self.replace_category_name_push_button.clicked.connect(self.replace_input_category_names)

        self.xml_data = None

    def find_category_names_for_replace(self, text):
        self.input_category_names_proxy_model.setFilterCaseSensitivity(Qt.CaseInsensitive)
        self.input_category_names_proxy_model.setFilterRegularExpression(text)
        input_category_names_count = self.input_category_names_proxy_model.rowCount()
        if (input_category_names_count == 0
                or text == ""
                or self.replace_category_name_line_edit.text() == ""):
            self.replace_category_name_push_button.setEnabled(False)
        else:
            self.replace_category_name_push_button.setEnabled(True)

    def replace_category_name_line_edit_text_change(self, text):
        if (self.input_category_names_proxy_model.rowCount() == 0
                or text == ""
                or self.replace_category_name_line_edit.text() == ""):
            self.replace_category_name_push_button.setEnabled(False)
        else:
            self.replace_category_name_push_button.setEnabled(True)

    def replace_input_category_names(self):
        rows_count = self.input_category_names_proxy_model.rowCount()
        for row in range(rows_count):
            item = self.input_category_names_proxy_model.data(self.input_category_names_proxy_model.index(row, 0),
                                                              Qt.DisplayRole)
            print(item)

    def find_product_names_for_replace(self, text):
        pass

    def replace_product_names(self):
        pass

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
        output_category_model = self.output_category_table_view.model().sourceModel()
        final_product_model = self.output_products_table_view.model().sourceModel()

        selected_categories_ids_list = []
        for row in range(output_category_model.rowCount()):
            chosen_category_id = output_category_model.data(output_category_model.index(row, 1))
            selected_categories_ids_list.append(chosen_category_id)

        chosen_products_ids_dict = {}
        for row in range(final_product_model.rowCount()):
            product_name = final_product_model.data(final_product_model.index(row, 0))
            wholesale_price = final_product_model.data(final_product_model.index(row, 2))
            drop_price = final_product_model.data(final_product_model.index(row, 3))
            product_id = final_product_model.data(final_product_model.index(row, 4))
            chosen_products_ids_dict[product_id] = {}
            chosen_products_ids_dict[product_id]["product_name"] = product_name
            if wholesale_price != 0:
                chosen_products_ids_dict[product_id]["wholesale_price"] = wholesale_price
            if drop_price != 0:
                chosen_products_ids_dict[product_id]["drop_price"] = drop_price

        # Create a copy of self.input_xml_tree
        self.output_xml_tree: ElementTree = copy.deepcopy(self.input_xml_tree)
        output_xml_tree = self.output_xml_tree
        if output_xml_tree is None:
            return

        # Remove unselected categories
        categories_elements_list = output_xml_tree.xpath("//category")
        for category in categories_elements_list:
            category_id = category.get("id").strip()
            if category_id not in selected_categories_ids_list:
                category.getparent().remove(category)

        # Remove products of unselected categories
        offers = output_xml_tree.xpath("//offer")
        for offer in offers:
            category_id = offer.xpath("categoryId")[0].text.strip()
            if category_id not in selected_categories_ids_list:
                offer.getparent().remove(offer)
                continue

        # Remove unselected products
        offers = output_xml_tree.xpath("//offer")
        for offer in offers:
            product_id = offer.get("id").strip()
            if product_id not in chosen_products_ids_dict.keys():
                offer.getparent().remove(offer)
            else:
                # Change price to new
                price = offer.xpath("url")[0]
                if "wholesale_price" in chosen_products_ids_dict[product_id].keys():
                    wholesale_price = chosen_products_ids_dict[product_id]["wholesale_price"]
                    price = offer.xpath("price")[0]
                    price.text = str(wholesale_price)

                if "drop_price" in chosen_products_ids_dict[product_id].keys():
                    drop_price = chosen_products_ids_dict[product_id]["drop_price"]
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
        if save_dialog.exec():
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

        # Get all categories ids from self.output_category_table_view
        output_category_model = self.output_category_table_view.model()
        categories_ids = list()
        for row in range(output_category_model.rowCount()):
            # Gather ids of the selected categories
            item = output_category_model.data(output_category_model.index(row, 1))
            categories_ids.append(item)

        # Gather all products ids from sptv_model in input_products_ids_list
        input_products_ids_list = list()
        for row in range(sptv_model.rowCount()):
            item = sptv_model.data(sptv_model.index(row, 1))
            input_products_ids_list.append(item)

        for category_id in categories_ids:
            products_list = self.all_category_ids_products_dict[category_id]
            for products_dict in products_list:
                product_name = products_dict["product_name"]
                if product_name in input_products_ids_list:
                    continue
                product_price = products_dict["product_price"]
                product_id = products_dict["product_id"]
                product_item = QStandardItem()
                product_item.setData(product_name, Qt.DisplayRole)
                product_item.setCheckable(True)
                price_item = QStandardItem()
                price_item.setData(product_price, Qt.DisplayRole)
                product_id_item = QStandardItem()
                product_id_item.setData(product_id, Qt.DisplayRole)
                sptv_model.sourceModel().appendRow([product_item, price_item, product_id_item])
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
        input_table_row_count = input_model.rowCount()
        input_col_count = input_model.columnCount()
        row = 0
        while row < input_table_row_count:
            checked = input_model.data(input_model.index(row, 0), Qt.CheckStateRole)
            if checked == 2:
                # Collect all 5 columns of data
                data = []
                for col in range(input_col_count):
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
        output_col_count = destination_model.columnCount()

        for row in range(output_col_count):

            # Collect all columns from destination model (assuming same structure)
            data = []
            for col in range(destination_model.columnCount()):
                data.append(destination_model.data(destination_model.index(row, col)))
            destination_results.append(data)

        # Add unique items from source to destination (considering all columns)
        for item_data in input_results:
            # Check if items id is existing in the destination model
            if item_data[-1] not in [result[-1] for result in destination_results]:
                # Check if columns count of the destination model is greater than the source model
                if output_col_count > input_col_count:
                    new_item = MainWindow.from_input_to_output_table(destination_model, input_col_count, item_data)
                elif output_col_count < input_col_count:
                    new_item = MainWindow.from_output_to_input_table(destination_model, output_col_count, item_data)
                destination_model.sourceModel().appendRow(new_item)
                print("Item", new_item, "has been removed")

        destination_tabel.resizeColumnsToContents()
        input_tabel.resizeColumnsToContents()
        print("The process of moving items has been completed.")
        print("Data has been added to table")

    @staticmethod
    def from_output_to_input_table(destination_model, input_col_count, item_data):
        new_item = []
        dst_col_count = destination_model.columnCount()
        for dst_col_num in range(dst_col_count):
            column_item = QStandardItem()
            if dst_col_num < dst_col_count - 1:
                column_item.setData(item_data[dst_col_num], Qt.DisplayRole)
            else:
                column_item.setData(item_data[-1], Qt.DisplayRole)
            column_item.setCheckable(True if dst_col_num == 0 else False)
            column_item.setEditable(False)
            new_item.append(column_item)
        return new_item

    @staticmethod
    def from_input_to_output_table(destination_model, input_col_count, item_data):
        new_item = []
        dst_col_count = destination_model.columnCount()
        # for value in item_data:
        for dst_col_num in range(dst_col_count):
            column_item = QStandardItem()
            if dst_col_num < input_col_count - 1:
                column_item.setData(item_data[dst_col_num], Qt.DisplayRole)
            else:
                if dst_col_num != dst_col_count - 1:
                    column_item.setData(0, Qt.DisplayRole)
                else:
                    column_item.setData(item_data[-1], Qt.DisplayRole)
            column_item.setCheckable(True if dst_col_num == 0 else False)
            column_item.setEditable(False)
            new_item.append(column_item)
        return new_item

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
                item_name = input_model.data(input_model.index(row, 0))
                item_id = input_model.data(input_model.index(row, 1))
                input_results.append([item_name, item_id])
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
            item = destination_model.data(destination_model.index(row, 1))
            destination_results.append(item)

        # Add unique items from source to destination
        for categoryname_id in input_results:
            categoryname_item = QStandardItem()
            c_name = categoryname_id[0]
            category_id = categoryname_id[1]
            categoryname_item.setData(c_name, Qt.DisplayRole)
            categoryname_item.setCheckable(True)
            categoryid_item = QStandardItem()
            categoryid_item.setData(category_id, Qt.DisplayRole)

            if category_id not in destination_results:
                destination_model.sourceModel().appendRow([categoryname_item, categoryid_item])
        destination_table_view.resizeColumnsToContents()
        print("The process of moving items has been completed.")

    # open xml file
    def open_file(self):
        file_path, _ = QFileDialog.getOpenFileName(filter="XML Files (*.xml)")
        category_ids_products_dict = self.parse(file_path)
        if not category_ids_products_dict:
            return
        self.all_category_ids_products_dict = category_ids_products_dict
        self.reset_tables_data()
        self.populate_input_tables()
        print("File closed")

    def reset_tables_data(self):
        self.input_category_model.removeRows(0, self.input_category_model.rowCount())
        self.output_category_model.removeRows(0, self.output_category_model.rowCount())

    def populate_input_tables(self):
        for category_id in self.all_category_ids_products_dict.keys():
            category_name = self.categoryid_name_dict[category_id]
            category_name_item = QStandardItem()
            category_name_item.setCheckable(True)
            category_name_item.setData(category_name, Qt.DisplayRole)
            category_id_item = QStandardItem()
            category_id_item.setData(category_id, Qt.DisplayRole)
            self.input_category_model.appendRow([category_name_item, category_id_item])

        all_products_list = []
        for product_names_list in self.all_category_ids_products_dict.values():
            all_products_list.extend(product_names_list)

        for product in all_products_list:
            product_name_item = QStandardItem()
            product_name = product["product_name"]
            product_name_item.setData(product_name, Qt.DisplayRole)
            product_id_item = QStandardItem()
            product_id = product["product_id"]
            product_id_item.setData(product_id, Qt.DisplayRole)
            self.input_product_names_model.appendRow([product_name_item, product_id_item])
        self.input_product_names_table_view.resizeColumnsToContents()

        # Make the same for the self.input_category_names_model
        for category_id, category_name in self.categoryid_name_dict.items():
            category_name_item = QStandardItem()
            category_name_item.setData(category_name, Qt.DisplayRole)
            category_id_item = QStandardItem()
            category_id_item.setData(category_id, Qt.DisplayRole)
            self.input_category_names_model.appendRow([category_name_item, category_id_item])
        self.input_category_names_table_view.resizeColumnsToContents()
        self.input_category_table_view.resizeColumnsToContents()

    def parse(self, file_path):
        if not file_path:
            return None
        parser = etree.XMLParser(encoding="windows-1251")
        self.input_xml_tree = etree.parse(file_path, parser=parser)
        category_elems = self.input_xml_tree.xpath("//category")
        categoryid_name_dict = {}

        for category in category_elems:
            category_id = category.get("id").strip()
            category_name = category.text.strip()
            categoryid_name_dict[category_id] = category_name
        self.categoryid_name_dict = categoryid_name_dict
        self.categoryid_name_dict[MainWindow.DEFAULT_CATEGORY_ID] = MainWindow.DEFAULT_CATEGORY_NAME

        category_products_dict = {}
        # TODO: change category names to category ids
        for category_id in categoryid_name_dict.keys():
            category_products_dict[category_id] = []

        # Add the category MainWindow.DEFAULT_CATEGORY for products without category
        category_products_dict[MainWindow.DEFAULT_CATEGORY_ID] = []

        offer_tags = self.input_xml_tree.xpath("//offer")
        for offer_tag in offer_tags:
            category_id = offer_tag.xpath("categoryId")
            product_id = offer_tag.get("id").strip()
            product_name = offer_tag.xpath("name")[0].text.strip()
            product_price = int(offer_tag.xpath("price")[0].text.strip())
            cid = category_id[0].text.strip()
            print(cid)
            if cid not in categoryid_name_dict:
                # Add product to the category MainWindow.DEFAULT_CATEGORY
                category_products_dict[MainWindow.DEFAULT_CATEGORY_ID].append(
                    {"product_id": product_id, "product_name": product_name, "product_price": product_price}
                )
                continue
            category_products_dict[cid].append(
                {"product_id": product_id, "product_name": product_name, "product_price": product_price}
            )
        pprint.pp(category_products_dict)

        # del tree, categories, offer_tags
        gc.collect()
        return category_products_dict

import copy
import gc
import pprint
import re
import networkx as nx

from PySide6.QtCore import QSortFilterProxyModel, QModelIndex
from PySide6.QtCore import Qt
from PySide6.QtGui import QStandardItemModel, QStandardItem
from PySide6.QtWidgets import QMainWindow, QFileDialog, QTableView, QHeaderView, QMessageBox, QTreeView
from lxml import etree
from lxml.etree import ElementTree

from ui_mainwindow import Ui_MainWindow


class MainWindow(QMainWindow, Ui_MainWindow):
    DEFAULT_CATEGORY_NAME = "Без категорії"
    DEFAULT_CATEGORY_ID = "-1"

    def __init__(self, app):
        super().__init__()
        self.cloned_parentid_items_dict = {}
        self.parentid_childid_dict = {}
        self.setupUi(self)
        self.app = app
        self.setWindowTitle("XML parser")
        self.block_parent_checkboxes_checking = False
        self.init_item = None
        self.block_sibling_checkboxes_checking = False

        self.categoryid_parent_ids_dict = {}
        # hint: dict[category_id] = category_name_item
        self.input_categories_dict: dict[str, QStandardItem] = {}
        # hint: dict[category_id] = category_name_item
        self.output_categories_dict: dict[str, QStandardItem] = {}
        # hint: self.input_products_dict[product_id].append({"category_id": product_id_item,
        #                                       "product_name": product_name_item,
        #                                       "product_price": product_price_item}
        self.input_products_dict: dict[str, dict[str:QStandardItem, str:QStandardItem, str:QStandardItem]] = {}
        self.output_products_dict: dict[str, dict[str:QStandardItem, str:QStandardItem, str:QStandardItem]] = {}
        self.input_categories_replacement_dict: dict[str, QStandardItem] = {}
        self.output_categories_replacement_dict: dict[str, dict[str: QStandardItem]] = {}
        self.input_products_replacement_dict: dict[str, QStandardItem] = {}
        self.output_products_replacement_dict: dict[str, dict[str: QStandardItem]] = {}

        # self.input_category_ids_products_dict: dict[str, list[dict[str:QStandardItem, str:QStandardItem, str:QStandardItem]]] = {}
        # self.output_category_ids_products_dict: dict[str, list[dict[str:QStandardItem, str:QStandardItem, str:QStandardItem]]] = {}
        self.input_xml_tree = None
        self.output_xml_tree = None

        # Init of input_category_table_view
        category_header_name = ["Категорія", "ID"]
        self.input_category_model = QStandardItemModel()
        self.input_category_model.setHorizontalHeaderLabels(category_header_name)
        self.input_category_proxy_model = QSortFilterProxyModel()
        self.input_category_proxy_model.setSourceModel(self.input_category_model)
        self.input_category_proxy_model.setFilterKeyColumn(0)
        self.input_category_tree_view.setModel(self.input_category_proxy_model)
        self.input_category_tree_view.resizeColumnToContents(0)
        # self.input_category_table_view.horizontalHeader().setStretchLastSection(True)
        # self.input_category_tree_view.horizontalHeader().setDefaultAlignment(Qt.AlignLeft)
        # noinspection PyUnresolvedReferences
        self.input_category_tree_view.setEditTriggers(QTableView.NoEditTriggers)

        # Init of output_category_table_view
        self.output_category_model = QStandardItemModel()
        self.output_category_model.setHorizontalHeaderLabels(category_header_name)
        self.output_category_proxy_model = QSortFilterProxyModel()
        self.output_category_proxy_model.setSourceModel(self.output_category_model)
        self.output_category_proxy_model.setFilterKeyColumn(0)
        self.output_category_tree_view.setModel(self.output_category_proxy_model)
        # self.output_category_table_view.horizontalHeader().setStretchLastSection(True)
        # self.output_category_tree_view.horizontalHeader().setDefaultAlignment(Qt.AlignLeft)
        # noinspection PyUnresolvedReferences
        self.output_category_tree_view.setEditTriggers(QTableView.NoEditTriggers)

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
        self.input_product_names_proxy_model = QSortFilterProxyModel()
        self.input_product_names_proxy_model.setSourceModel(self.input_product_names_model)
        self.input_product_names_proxy_model.setFilterKeyColumn(0)
        self.input_product_names_table_view.setModel(self.input_product_names_proxy_model)
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
            lambda: self.move_categories_between_tables(self.input_category_tree_view,
                                                        self.output_category_tree_view)
        )
        self.delete_category_push_button.clicked.connect(
            lambda: self.move_categories_between_tables(self.output_category_tree_view,
                                                        self.input_category_tree_view))

        self.output_category_model.rowsInserted.connect(self.populate_input_products_table)
        self.add_product_push_button.clicked.connect(
            lambda: self.move_products_between_tables(
                self.input_products_table_view, self.output_products_table_view)
        )
        self.remove_product_push_button.clicked.connect(
            lambda: self.move_products_between_tables(
                self.output_products_table_view, self.input_products_table_view)
        )
        self.output_category_model.rowsAboutToBeRemoved.connect(self.refresh_products_tables)
        self.input_category_tree_view.expanded.connect(lambda: self.input_category_tree_view.resizeColumnToContents(0))
        self.output_category_tree_view.expanded.connect(
            lambda: self.output_category_tree_view.resizeColumnToContents(0))
        self.input_category_tree_view.collapsed.connect(lambda: self.input_category_tree_view.resizeColumnToContents(0))
        self.output_category_tree_view.collapsed.connect(
            lambda: self.output_category_tree_view.resizeColumnToContents(0))
        self.apply_multiplier_push_button.clicked.connect(self.apply_multiplier)
        self.get_new_xml_push_button.clicked.connect(self.get_new_xml)
        self.bottom_price_limit_spin_box.valueChanged.connect(self.checkForBottomPriceValue)
        self.upper_price_limit_spin_box.valueChanged.connect(self.checkForUpperPriceValue)
        self.action_about_qt.triggered.connect(self.about_qt)

        self.search_category_for_replace_line_edit.textChanged.connect(self.find_category_names_for_replace)
        self.replace_category_name_line_edit.textChanged.connect(self.replace_category_name_line_edit_text_change)
        self.replace_category_name_push_button.setEnabled(False)
        self.replace_category_name_push_button.clicked.connect(self.replace_input_category_names)

        self.search_product_for_replace_line_edit.textChanged.connect(self.find_product_names_for_replace)
        self.replace_product_name_line_edit.textChanged.connect(self.replace_product_name_line_edit_text_change)
        self.replace_product_name_push_button.setEnabled(False)
        self.replace_product_name_push_button.clicked.connect(self.replace_input_product_names)

        # self.input_category_tree_view.clicked.connect(self.on_clicked_check_for_subcategories)
        self.input_category_model.itemChanged.connect(self.on_clicked_check_for_subcategories)
        self.output_category_model.itemChanged.connect(self.on_clicked_check_for_subcategories)

        self.xml_data = None

    def on_clicked_check_for_subcategories(self, item):
        if self.block_parent_checkboxes_checking is False:
            self.block_parent_checkboxes_checking = True
            current_item_checkbox_state = item.checkState()
            self.iterate_tree(current_item_checkbox_state, item)
            current_item = item.parent()
            # while current_item is not None:
            #     current_item.setCheckState(current_item_checkbox_state)
            #     current_item = current_item.parent()
            ###########################################
            current_item = item
            while current_item.parent() is not None:
                current_item_checkbox_state = current_item.checkState()
                is_change_parent_checkboxes_state = True
                sibling_count = current_item.parent().rowCount()
                for row in range(sibling_count):
                    sibling_item_checkbox_state = current_item.parent().child(row).checkState()
                    if current_item_checkbox_state != sibling_item_checkbox_state:
                        current_item.parent().setCheckState(Qt.CheckState.PartiallyChecked)
                        is_change_parent_checkboxes_state = False
                        break
                if is_change_parent_checkboxes_state is True:
                    current_item.parent().setCheckState(current_item_checkbox_state)
                current_item = current_item.parent()

            self.block_parent_checkboxes_checking = False

    def iterate_tree(self, checkbox_state, item):
        if item.hasChildren():
            for row in range(item.rowCount()):
                child_item = item.child(row)
                self.iterate_tree(checkbox_state, child_item)
        item.setCheckState(checkbox_state)

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

    def find_product_names_for_replace(self, text):
        self.input_product_names_proxy_model.setFilterCaseSensitivity(Qt.CaseInsensitive)
        self.input_product_names_proxy_model.setFilterRegularExpression(text)
        input_product_count = self.input_product_names_proxy_model.rowCount()
        if (input_product_count == 0
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

    def checkForUpperPriceValue(self, value):
        if value < self.bottom_price_limit_spin_box.value():
            self.upper_price_limit_spin_box.setValue(self.upper_price_limit_spin_box.value() + 1)
            # noinspection PyUnresolvedReferences
            QMessageBox.warning(self, "Попередження",
                                "Верхня межа не може бути менше за нижню!",
                                QMessageBox.Ok)

    def get_new_xml(self):
        output_category_model = self.output_category_tree_view.model().sourceModel()
        final_product_model = self.output_products_table_view.model().sourceModel()

        selected_categories_ids_list = []
        for row in range(output_category_model.rowCount()):
            chosen_category_id = output_category_model.data(output_category_model.index(row, 1))
            selected_categories_ids_list.append(chosen_category_id)

        chosen_id_products_dict = {}
        for row in range(final_product_model.rowCount()):
            product_name = final_product_model.data(final_product_model.index(row, 0))
            wholesale_price = final_product_model.data(final_product_model.index(row, 2))
            drop_price = final_product_model.data(final_product_model.index(row, 3))
            product_id = final_product_model.data(final_product_model.index(row, 4))
            chosen_id_products_dict[product_id] = {}
            chosen_id_products_dict[product_id]["product_name"] = product_name
            if wholesale_price != 0:
                chosen_id_products_dict[product_id]["wholesale_price"] = wholesale_price
            if drop_price != 0:
                chosen_id_products_dict[product_id]["drop_price"] = drop_price

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
            if product_id not in chosen_id_products_dict.keys():
                offer.getparent().remove(offer)
            else:
                # Change price to new
                price = offer.xpath("url")[0]
                if "wholesale_price" in chosen_id_products_dict[product_id].keys():
                    wholesale_price = chosen_id_products_dict[product_id]["wholesale_price"]
                    price = offer.xpath("price")[0]
                    price.text = str(wholesale_price)

                if "drop_price" in chosen_id_products_dict[product_id].keys():
                    drop_price = chosen_id_products_dict[product_id]["drop_price"]
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
            # final_price = fptv_model.data(fptv_model.index(row, column_index_target_price))
            if bottom_price_limit <= input_price <= upper_price_limit:
                product_markup = int(multiplier * input_price)
                fptv_model.setData(fptv_model.index(row, column_index_target_price), product_markup)
            print(input_price)

    def populate_input_products_table(self):
        sptv_model = self.input_products_table_view.model().sourceModel()
        output_category_model = self.output_category_tree_view.model()

        selected_categories_ids = list()
        row_count = output_category_model.rowCount()
        for row in range(row_count):
            # TODO: Recursively get all selected categories
            # Gather ids of the selected categories
            item = output_category_model.data(output_category_model.index(row, 1))
            selected_categories_ids.append(item)

        # Gather all products ids from sptv_model in input_products_ids_list
        input_products_ids_list = list()
        for row in range(sptv_model.rowCount()):
            item = sptv_model.data(sptv_model.index(row, 1))
            input_products_ids_list.append(item)

        for product_id, product_items in self.input_products_dict.items():
            product_id_item = QStandardItem(product_id)
            product_name_item = product_items["product_name"]
            product_price_item = product_items["product_price"]
            category_id = product_items["category_id"].data(Qt.DisplayRole)
            if category_id in selected_categories_ids:
                sptv_model.appendRow([product_name_item, product_price_item, product_id_item])
        self.input_products_table_view.resizeColumnsToContents()
        # self.input_products_table_view.horizontalHeader().setStretchLastSection(True)
        print("Data has been added to table")

    @staticmethod
    def move_products_between_tables(input_tabel, output_tabel):
        input_model = input_tabel.model().sourceModel()
        output_model = output_tabel.model().sourceModel()
        # Check for destination model existence
        if not input_model or not output_model:
            print("Error: Invalid table view models.")
            return

        # Collect checked items in source model
        input_table_row_count = input_model.rowCount()
        input_col_count = input_model.columnCount()
        input_table_dict: dict[str, list[QModelIndex]] = dict()

        for col in range(input_col_count):
            input_table_dict[input_model.headerData(col, Qt.Horizontal)] = []

        row = 0
        checked_number = 0
        while row < input_table_row_count:
            check_state = input_model.item(row, 0).checkState()
            if check_state == Qt.Checked:
                checked_number += 1
                item_data = input_model.item(row, 0)
                item_data.setCheckState(Qt.Unchecked)
                for col in range(input_col_count):
                    item_data = input_model.takeItem(row, col)
                    header_name = input_model.headerData(col, Qt.Horizontal)
                    input_table_dict[header_name].append(item_data.data(Qt.DisplayRole))
                input_model.removeRow(row)
                input_table_row_count -= 1
            else:
                row += 1

        output_table_col_count = output_model.columnCount()
        output_table_dict: dict[int, str] = dict()
        for col in range(output_table_col_count):
            output_table_dict[col] = output_model.headerData(col, Qt.Horizontal)

        for row in range(checked_number):
            out_table_row_items = []
            for col in range(output_table_col_count):
                out_col_name = output_table_dict[col]
                new_item = QStandardItem()

                if out_col_name in input_table_dict:
                    new_item.setData(input_table_dict[out_col_name][row], Qt.DisplayRole)
                else:
                    new_item.setData(0, Qt.DisplayRole)

                new_item.setCheckable(True if col == 0 else False)
                new_item.setEditable(False)
                out_table_row_items.append(new_item)
            output_model.appendRow(out_table_row_items)

        input_tabel.resizeColumnsToContents()
        output_tabel.resizeColumnsToContents()
        print("The process of moving items has been completed.")
        print("Data has been added to table")

    def refresh_products_tables(self):
        output_categories_table_model = self.output_category_tree_view.model().sourceModel()
        row_count = output_categories_table_model.rowCount()
        output_category_id_list = []
        for row in range(row_count - 1):
            category_id = output_categories_table_model.item(row, 1).data(Qt.DisplayRole)
            output_category_id_list.append(category_id)

        input_products_model = self.input_products_table_view.model().sourceModel()
        input_table_col_count = input_products_model.columnCount()
        input_table_row_count = input_products_model.rowCount()
        row = 0
        while row < input_table_row_count:
            product_item = input_products_model.item(row, input_table_col_count - 1)
            product_id = product_item.data(Qt.DisplayRole)
            product_category_id = self.input_products_dict[product_id]["category_id"].data(Qt.DisplayRole)
            if product_category_id not in output_category_id_list:
                row_items = input_products_model.takeRow(row)
                name_item = row_items[0]
                name_item.setCheckState(Qt.Unchecked)
                input_table_row_count -= 1
            else:
                row += 1

        output_products_model = self.output_products_table_view.model().sourceModel()
        output_table_col_count = output_products_model.columnCount()
        output_table_row_count = output_products_model.rowCount()
        row = 0
        while row < output_table_row_count:
            product_id = output_products_model.item(row, output_table_col_count - 1).data(Qt.DisplayRole)
            product_category_id = self.input_products_dict[product_id]["category_id"].data(Qt.DisplayRole)
            if product_category_id not in output_category_id_list:
                row_items = output_products_model.takeRow(row)
                name_item = row_items[0]
                name_item.setCheckState(Qt.Unchecked)
                output_table_row_count -= 1
            else:
                row += 1
        print("Data has been removed from table")

    def move_categories_between_tables(self,
                                       input_category_tree_view: QTreeView,
                                       output_category_tree_view: QTreeView):
        """
        Moves checked items from the source table view to the destination table view.

        Args:
            input_table_view (QtWidgets.QTableView): The source table view.
            output_table_view (QtWidgets.QTableView): The destination table view.
            :param output_category_tree_view:
            :param input_category_tree_view:
        """
        # Get source and destination models
        input_model = input_category_tree_view.model().sourceModel()
        output_model = output_category_tree_view.model().sourceModel()

        if not input_model or not output_model:
            print("Error: Invalid table view models.")
            return

        # Collect checked items in source model
        row = 0
        while row < input_model.rowCount():
            input_item_name = input_model.item(row, 0)
            self.remove_item_from_input_table(input_item_name)
            row += 1

        row = 0
        while row < output_model.rowCount():
            output_item_name = output_model.item(row, 0)
            print("input_item_name: ", output_item_name.data(Qt.DisplayRole))
            self.iterate_output_category_tree_and_insert(output_item_name)
            row += 1

        # pprint.pp(f"output_items: {selected_items}")
        output_category_tree_view.resizeColumnToContents(0)
        print("The process of moving items has been completed.")

    def remove_item_from_input_table(self, input_item: QStandardItem):
        check_state: Qt.CheckState = input_item.checkState()
        if check_state != Qt.Unchecked:
            clone_name_item = QStandardItem(input_item)
            clone_name_item.setCheckable(True)
            clone_id_item = QStandardItem()
            # print("input_item name clone: ", input_item.data(Qt.DisplayRole))
            # print("input_item id clone: ", input_item.index().siblingAtColumn(1).data(Qt.DisplayRole))
            id_text = input_item.index().siblingAtColumn(1).data(Qt.DisplayRole)
            clone_id_item.setText(id_text)
            clone_id_item.setCheckable(False)
            if input_item.hasChildren():
                row = 0
                while row < input_item.rowCount():
                    child = input_item.child(row)
                    clone_child_name, clone_child_id_item = self.remove_item_from_input_table(child)
                    if clone_child_name is not None:
                        parent_id = self.categoryid_parent_ids_dict[clone_child_id_item.data(Qt.DisplayRole)]
                        if parent_id is not None:
                            if parent_id not in self.cloned_parentid_items_dict:
                                self.cloned_parentid_items_dict[parent_id] = []
                            self.cloned_parentid_items_dict[parent_id].append({"name": clone_child_name,
                                                                               "id": clone_child_id_item})
                            print("Checkstate: ", clone_child_name.checkState())
                    if child.checkState() == Qt.Checked:
                        input_item.removeRow(row)
                    else:
                        row += 1
            return clone_name_item, clone_id_item
        return None, None

    def iterate_output_category_tree_and_insert(self, output_item_name: QStandardItem):
        output_text_id = output_item_name.index().siblingAtColumn(1).data(Qt.DisplayRole)
        # for row in range(output_item_name.rowCount()):
        #     child = output_item_name.child(row, 0)
        #     self.iterate_output_category_tree_and_insert(child)
        items_list = []
        for row in range(output_item_name.rowCount()):
            child_id = output_item_name.child(row, 1)
            items_list.append(child_id.data(Qt.DisplayRole))

        if output_text_id in self.cloned_parentid_items_dict:
            input_items_list = self.cloned_parentid_items_dict.pop(output_text_id)
            for cloned_item in input_items_list:
                cloned_name_item = cloned_item["name"].clone()
                cloned_id_item = cloned_item["id"].clone()
                # b = True
                # for row in range(output_item_name.rowCount()):
                #     child_id = output_item_name.child(row, 1)
                #     if child_id.data(Qt.DisplayRole) == cloned_id_item.data(Qt.DisplayRole):
                #         b = False
                #         break
                # if b:
                if cloned_id_item.data(Qt.DisplayRole) not in items_list:
                    output_item_name.appendRow([cloned_name_item, cloned_id_item])
                for row in range(output_item_name.rowCount()):
                    child = output_item_name.child(row, 0)
                    self.iterate_output_category_tree_and_insert(child)

    # open xml file
    def open_file(self):
        file_path, _ = QFileDialog.getOpenFileName(filter="XML Files (*.xml)")
        self.init_tables(file_path)
        print("File closed")

    def init_tables(self, file_path):
        if not self.parse(file_path):
            return
        self.reset_input_categories_tables_data()
        self.populate_input_tables()

    def reset_input_categories_tables_data(self):
        self.input_category_model.removeRows(0, self.input_category_model.rowCount())
        self.output_category_model.removeRows(0, self.output_category_model.rowCount())

    def populate_input_tables(self):
        self.populate_category_tables()
        self.populate_input_categories_replacement_table()
        self.populate_input_products_replacement_table()

    def populate_input_products_replacement_table(self):
        for product_id_item, product_data in self.input_products_replacement_dict.items():
            product_id_item = QStandardItem()
            product_id_item.setData(product_id_item, Qt.DisplayRole)
            self.input_product_names_model.appendRow([product_data, product_id_item])
        self.input_product_names_table_view.resizeColumnsToContents()

    def populate_input_categories_replacement_table(self):
        for category_id, category_name_item in self.input_categories_replacement_dict.items():
            category_id_item = QStandardItem()
            category_id_item.setData(category_id, Qt.DisplayRole)
            self.input_category_names_model.appendRow([category_name_item, category_id_item])
        self.input_category_names_table_view.resizeColumnsToContents()

    def parse(self, file_path):
        if not file_path:
            return False
        parser = etree.XMLParser(encoding="windows-1251")
        self.input_xml_tree = etree.parse(file_path, parser=parser)
        self.get_category_ids_and_names_from_xml()
        self.get_offers_from_xml()
        gc.collect()
        pprint.pp(f"input_products_dict: {self.input_products_dict}")
        return True

    def get_offers_from_xml(self):
        offer_tags = self.input_xml_tree.xpath("//offer")
        for offer_tag in offer_tags:
            category_id_item, product_id, product_name_item, product_price_item = self.create_product(offer_tag)
            print("product_id: ", product_id)
            self.input_products_dict[product_id] = {"product_name": product_name_item,
                                                    "product_price": product_price_item,
                                                    "category_id": category_id_item, }
            product_name_item = self.create_product_name_item(offer_tag)
            self.input_products_replacement_dict[product_id] = product_name_item

    def get_category_ids_and_names_from_xml(self):
        category_elems = self.input_xml_tree.xpath("//category")
        for category in category_elems:
            category_id, category_name_item = self.create_category_item(category)
            self.categoryid_parent_ids_dict[category_id] = category.get("parentId")
            self.input_categories_dict[category_id] = category_name_item
            category_id, category_name_item = self.create_category_item(category)
            self.input_categories_replacement_dict[category_id] = category_name_item

    def create_product(self, offer_tag):
        product_id = offer_tag.get("id").strip()
        category_id = offer_tag.xpath("categoryId")[0].text.strip()
        category_id_item = QStandardItem()
        category_id_item.setData(category_id, Qt.DisplayRole)
        product_name_item = self.create_product_name_item(offer_tag)
        product_price = int(offer_tag.xpath("price")[0].text.strip())
        product_price_item = QStandardItem()
        product_price_item.setData(product_price, Qt.DisplayRole)
        return category_id_item, product_id, product_name_item, product_price_item

    @staticmethod
    def create_product_name_item(offer_tag):
        product_name = offer_tag.xpath("name")[0].text.strip()
        product_name_item = QStandardItem()
        product_name_item.setData(product_name, Qt.DisplayRole)
        product_name_item.setCheckable(True)
        return product_name_item

    @staticmethod
    def create_category_item(category):
        category_id = category.get("id").strip()
        category_name = category.text.strip()
        category_name_item: QStandardItem = QStandardItem()
        category_name_item.setCheckable(True)
        category_name_item.setData(category_name, Qt.DisplayRole)
        return category_id, category_name_item

    def populate_category_tables(self):
        # create a method that builds a tree of categories and subcategories from self.input_categories_dict
        graph = nx.DiGraph()
        parents_list = []
        # self.parentid_childid_dict = dict.fromkeys(self.categoryid_parent_ids_dict.values(), [])
        for child_id, parent_id in self.categoryid_parent_ids_dict.items():
            if parent_id is None:
                graph.add_node(child_id)
                parents_list.append(child_id)
                self.parentid_childid_dict[child_id] = []
            else:
                # self.parentid_childid_dict[parent_id].append(child_id)
                if parent_id not in self.parentid_childid_dict:
                    self.parentid_childid_dict[parent_id] = []
                self.parentid_childid_dict[parent_id].append(child_id)
                graph.add_node(parent_id)
                graph.add_node(child_id)
                graph.add_edge(parent_id, child_id)

        for parent_id in parents_list:
            input_item = self.input_categories_dict[parent_id]
            self.input_category_model.appendRow([input_item, QStandardItem(parent_id)])
            output_item = QStandardItem(input_item)
            self.output_category_model.appendRow([output_item, QStandardItem(parent_id)])
            self.dfs(graph, parent_id, input_item)
        self.input_category_tree_view.resizeColumnToContents(0)
        self.input_category_names_table_view.resizeColumnToContents(0)

    def dfs(self, graph, child_id, parent_item, indent=0):
        print(" " * indent, parent_item.data(Qt.DisplayRole))
        for child_id in graph.neighbors(child_id):
            item = self.input_categories_dict[child_id]
            parent_item.appendRow([item, QStandardItem(child_id)])
            self.dfs(graph, child_id, item, indent + 2)

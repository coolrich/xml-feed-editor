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
        self.setWindowTitle("XML parser")
        self.setupUi(self)
        self.app = app

        self.selected_categories_ids = []
        self.input_products_ids = []
        self.cloned_parentid_items_dict = {}
        self.parentid_childid_dict = {}
        self.block_parent_checkboxes_checking = False

        # Important
        self.categoryid_parent_ids_dict = {}
        # hint: dict[category_id] = category_name_item
        # Important
        self.input_categories_dict: dict[str, str] = {}
        # hint: dict[category_id] = category_name_item
        # self.output_categories_dict: dict[str, QStandardItem] = {}
        # hint: self.input_products_dict[product_id].append({"category_id": product_id_item,
        #                                       "product_name": product_name_item,
        #                                       "product_price": product_price_item}
        # important
        self.input_products_dict: dict[str, dict[str:QStandardItem, str:QStandardItem, str:QStandardItem]] = {}
        # important
        self.input_categories_replacement_dict: dict[str, QStandardItem] = {}
        # important
        self.output_categories_replacement_dict: dict[str, dict[str: QStandardItem]] = {}
        # important
        self.input_products_replacement_dict: dict[str, QStandardItem] = {}
        # important
        self.output_products_replacement_dict: dict[str, dict[str: QStandardItem]] = {}
        # important
        self.input_xml_tree = None
        self.output_xml_tree = None

        # Init of input_category_table_view
        category_header_name = ["Категорія", "ID"]
        self.input_category_model = QStandardItemModel()
        self.input_category_model.setHorizontalHeaderLabels(category_header_name)
        self.input_category_proxy_model = QSortFilterProxyModel()
        self.input_category_proxy_model.setRecursiveFilteringEnabled(True)
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
        self.output_category_proxy_model.setRecursiveFilteringEnabled(True)
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
        # self.add_category_push_button.clicked.connect(self.populate_input_products_table)
        self.delete_category_push_button.clicked.connect(
            lambda: self.move_categories_between_tables(self.output_category_tree_view,
                                                        self.input_category_tree_view))
        # self.delete_category_push_button.clicked.connect(self.refresh_products_tables)
        # self.output_category_model.rowsInserted.connect(self.populate_input_products_table)
        self.add_product_push_button.clicked.connect(
            lambda: self.move_products_between_tables(
                self.input_products_table_view, self.output_products_table_view)
        )
        # self.add_product_push_button.clicked.connect(self.populate_input_products_table)
        self.remove_product_push_button.clicked.connect(
            lambda: self.move_products_between_tables(
                self.output_products_table_view, self.input_products_table_view)
        )
        # self.remove_product_push_button.clicked.connect(self.refresh_products_tables)
        # self.output_category_model.rowsAboutToBeRemoved.connect(self.refresh_products_tables)
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
        self.replace_category_name_push_button.clicked.connect(self.replace_category_names)

        self.search_product_for_replace_line_edit.textChanged.connect(self.find_product_names_for_replace)
        self.replace_product_name_line_edit.textChanged.connect(self.replace_product_name_line_edit_text_change)
        self.replace_product_name_push_button.setEnabled(False)
        self.replace_product_name_push_button.clicked.connect(self.replace_product_names)
        self.check_all_input_products_push_button.clicked.connect(
            lambda: self.select_all_products(self.input_products_model, True)
        )
        self.uncheck_all_input_products_push_button.clicked.connect(
            lambda: self.select_all_products(self.input_products_model, False)
        )
        self.check_all_output_products_push_button.clicked.connect(
            lambda: self.select_all_products(self.output_products_model, True)
        )
        self.uncheck_all_output_products_push_button.clicked.connect(
            lambda: self.select_all_products(self.output_products_model, False)
        )

        self.check_all_input_categories_push_button.clicked.connect(
            lambda: self.select_all_categories(self.input_category_model, True)
        )
        self.uncheck_all_input_categories_push_button.clicked.connect(
            lambda: self.select_all_categories(self.input_category_model, False)
        )

        self.check_all_output_categories_push_button.clicked.connect(
            lambda: self.select_all_categories(self.output_category_model, True)
        )
        self.uncheck_all_output_categories_push_button.clicked.connect(
            lambda: self.select_all_categories(self.output_category_model, False)
        )
        self.input_category_model.itemChanged.connect(self.on_clicked_check_for_subcategories)
        self.output_category_model.itemChanged.connect(self.on_clicked_check_for_subcategories)

        self.xml_data = None

    @staticmethod
    def select_all_products(model, checked):
        row_count = model.rowCount()
        for row in range(row_count):
            if checked:
                model.item(row, 0).setCheckState(Qt.Checked)
            else:
                model.item(row, 0).setCheckState(Qt.Unchecked)

    @staticmethod
    def select_all_categories(model, checked):
        row_count = model.rowCount()
        for row in range(row_count):
            if checked:
                model.item(row, 0).setCheckState(Qt.Checked)
            else:
                model.item(row, 0).setCheckState(Qt.Unchecked)

    def replace_category_names(self):
        old_category_name = self.search_category_for_replace_line_edit.text()
        new_category_name = self.replace_category_name_line_edit.text()

        category_ids = []
        for category_id, category_item_name in self.input_categories_replacement_dict.items():
            category_name = category_item_name.data(Qt.DisplayRole)
            if old_category_name in category_name:
                category_ids.append(category_id)
        pprint.pp(category_ids)

        self.replace_words_in_input_categories_dict(category_ids, old_category_name, new_category_name)
        self.replace_words_in_tree_categories_table(self.input_category_model, category_ids)
        self.replace_words_in_tree_categories_table(self.output_category_model, category_ids)
        self.__replace_category_words_in_output_xml_tree(category_ids)

    def replace_product_names(self):
        old_product_name = self.search_product_for_replace_line_edit.text()
        new_product_name = self.replace_product_name_line_edit.text()
        product_ids_description = self.get_products_description_ids(old_product_name)
        product_ids_names = self.get_products_names_ids(old_product_name)
        for product_id, product_item_name in self.input_products_dict.items():
            product_name = product_item_name["product_name"].data(Qt.DisplayRole)
            if product_id in product_ids_names:
                print("-----------------", "-" * len(product_name), sep="")
                print("Old product name:", product_name)
                while old_product_name in product_name:
                    product_name = product_name.replace(old_product_name, new_product_name)
                print("New product name:", product_name)
                product_item_name["product_name"].setData(product_name, Qt.DisplayRole)
        product_ids = set()
        product_ids.update(product_ids_names)
        product_ids.update(product_ids_description)
        self.replace_words_in_input_product_names_table(product_ids_names)
        self.__replace_product_words_in_output_xml_tree(product_ids)

    def replace_words_in_input_product_names_table(self, category_ids):
        for product_id, product_item_name in self.input_products_replacement_dict.items():
            product_item_name = self.input_products_dict[product_id]["product_name"].data(Qt.DisplayRole)
            if product_id in category_ids:
                self.input_products_replacement_dict[product_id].setText(product_item_name)

    def __replace_product_words_in_output_xml_tree(self, product_ids):
        output_xml_tree = self.output_xml_tree
        offers_elements_list = output_xml_tree.xpath("//offer")
        for offer in offers_elements_list:
            product_id = offer.get("id")
            if product_id in product_ids:
                # ts000027787
                # TODO: which tags content should be changed
                self.change_name_tag(offer, product_id)
                # TODO: description tag should be changed
                description_tag, description_text = self.change_description_tag(offer)
                if description_text is not None and len(description_text) > 0:
                    description_tag.text = description_text

        pprint.pp(offers_elements_list[0])

    def change_description_tag(self, offer):
        description_tag = offer.xpath("description")[0]
        description_text = description_tag.text
        description_text = self.find_and_replace_in_description_tag(description_text)
        return description_tag, description_text

    def change_name_tag(self, offer, product_id):
        product_name_tag = offer.xpath("name")[0]
        product_name = self.input_products_dict[product_id]["product_name"].data(Qt.DisplayRole)
        product_name_tag.text = product_name

    def find_and_replace_in_description_tag(self, description_tag_text):
        old_product_name = self.search_product_for_replace_line_edit.text()
        new_product_name = self.replace_product_name_line_edit.text()
        if description_tag_text is None:
            return None
        while old_product_name in description_tag_text:
            description_tag_text = description_tag_text.replace(old_product_name, new_product_name)
        return description_tag_text

    def __replace_category_words_in_output_xml_tree(self, category_ids):
        output_xml_tree = self.output_xml_tree
        categories_elements_list = output_xml_tree.xpath("//category")
        for category in categories_elements_list:
            category_id = category.get("id")
            if category_id in category_ids:
                category.text = self.input_categories_dict[category_id]

    def replace_words_in_tree_categories_table(self, input_model, category_ids):
        row_count = input_model.rowCount()
        for row in range(row_count):
            name_item = input_model.item(row, 0)
            self.check_id_and_change(category_ids, name_item)
            self.iterate_categories_tree_and_replace_words(name_item, category_ids)

    def check_id_and_change(self, category_ids, name_item):
        id_item_value = name_item.index().siblingAtColumn(1).data(Qt.DisplayRole)
        if id_item_value in category_ids:
            new_item_name = self.input_categories_dict[id_item_value]
            name_item.setData(new_item_name, Qt.DisplayRole)

    def iterate_categories_tree_and_replace_words(self, name_item, category_ids):
        if name_item.hasChildren():
            for i in range(name_item.rowCount()):
                child_item = name_item.child(i)
                self.check_id_and_change(category_ids, child_item)
                self.iterate_categories_tree_and_replace_words(child_item, category_ids)

    def replace_words_in_input_categories_dict(self, category_ids, old_category_name: str, new_category_name: str):
        print("Replaced words in input input_categories_dict:")
        for category_id in category_ids:
            category_name = self.input_categories_dict[category_id]
            print("Old category:", category_name)
            while old_category_name in category_name:
                category_name = category_name.replace(old_category_name, new_category_name)
            print("New category:", category_name)
            print("--" * len(category_name))
            self.input_categories_dict[category_id] = category_name
            # TODO: pay attention to here.
            self.input_categories_replacement_dict[category_id].setData(category_name, Qt.DisplayRole)

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
            self.bottom_price_limit_spin_box.setValue(self.upper_price_limit_spin_box.value())
            # Show a warning window with message Нижня межа не може перевищувати верхню
            # noinspection PyUnresolvedReferences
            QMessageBox.warning(self, "Попередження",
                                "Нижня межа не може перевищувати верхню",
                                QMessageBox.Ok)

    def checkForUpperPriceValue(self, value):
        if value < self.bottom_price_limit_spin_box.value():
            self.upper_price_limit_spin_box.setValue(self.bottom_price_limit_spin_box.value())
            # noinspection PyUnresolvedReferences
            QMessageBox.warning(self, "Попередження",
                                "Верхня межа не може бути менше за нижню!",
                                QMessageBox.Ok)

    def get_new_xml(self):
        # output_category_model = self.output_category_tree_view.model().sourceModel()
        final_product_model = self.output_products_table_view.model().sourceModel()

        if self.output_xml_tree is None:
            return
        output_xml_tree = self.output_xml_tree

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

        # Remove unselected categories
        categories_elements_list = output_xml_tree.xpath("//category")
        for category in categories_elements_list:
            category_id = category.get("id").strip()
            if category_id not in self.selected_categories_ids:
                category.getparent().remove(category)

        # Remove products of unselected categories
        offers = output_xml_tree.xpath("//offer")
        for offer in offers:
            category_id = offer.xpath("categoryId")[0].text.strip()
            if category_id not in self.selected_categories_ids:
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
        output_category_model = self.output_category_tree_view.model().sourceModel()

        self.selected_categories_ids = list()
        row_count = output_category_model.rowCount()
        for row in range(row_count):
            item = output_category_model.item(row, 0)
            self.get_selected_categories(item)
        print("Selected categories:", self.selected_categories_ids)

        for product_id, product_items in self.input_products_dict.items():
            product_id_item = QStandardItem(product_id)
            product_name_item = product_items["product_name"]
            product_price_item = product_items["product_price"]
            category_id = product_items["category_id"].data(Qt.DisplayRole)
            product_id_text = product_id_item.data(Qt.DisplayRole)
            if category_id in self.selected_categories_ids and product_id_text not in self.input_products_ids:
                self.input_products_ids.append(product_id)
                sptv_model.appendRow([product_name_item, product_price_item, product_id_item])
        self.input_products_table_view.resizeColumnsToContents()
        # self.input_products_table_view.horizontalHeader().setStretchLastSection(True)
        print("Data has been added to table")

    def get_selected_categories(self, output_item):
        row_count = output_item.rowCount()
        self.selected_categories_ids.append(output_item.index().siblingAtColumn(1).data(Qt.DisplayRole))
        print("Item id:", output_item.data(Qt.DisplayRole), "Row count:", row_count)
        for row in range(row_count):
            self.get_selected_categories(output_item.child(row, 0))

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
                    input_table_dict[header_name].append(item_data)
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
                if out_col_name in input_table_dict:
                    new_item = input_table_dict[out_col_name][row]
                    out_table_row_items.append(new_item)
                else:
                    new_item = QStandardItem()
                    new_item.setData(0, Qt.DisplayRole)
                    out_table_row_items.append(new_item)

                new_item.setCheckable(True if col == 0 else False)
                new_item.setEditable(False)
            output_model.appendRow(out_table_row_items)

        input_tabel.resizeColumnsToContents()
        output_tabel.resizeColumnsToContents()
        print("The process of moving items has been completed.")
        print("Data has been added to table")

    def refresh_products_tables(self):
        input_products_model = self.input_products_table_view.model().sourceModel()
        input_table_col_count = input_products_model.columnCount()
        input_table_row_count = input_products_model.rowCount()

        row = 0
        while row < input_products_model.rowCount():
            product_item = input_products_model.item(row, input_table_col_count - 1)
            product_id = product_item.data(Qt.DisplayRole)
            product_category_id = self.input_products_dict[product_id]["category_id"].data(Qt.DisplayRole)
            if product_category_id not in self.selected_categories_ids:
                row_items = input_products_model.takeRow(row)
                name_item = row_items[0]
                name_item.setCheckState(Qt.Unchecked)
                self.input_products_ids.remove(product_id)
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
            if product_category_id not in self.selected_categories_ids:
                row_items = output_products_model.takeRow(row)
                name_item = row_items[0]
                name_item.setCheckState(Qt.Unchecked)
                self.input_products_ids.remove(product_id)
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

        row = 0
        output_item_ids = []
        while row < output_model.rowCount():
            output_item_id = output_model.item(row, 1).data(Qt.DisplayRole)
            output_item_ids.append(output_item_id)
            row += 1

        row = 0
        while row < input_model.rowCount():
            input_item_name = input_model.item(row, 0)

            if input_item_name.checkState() != Qt.Unchecked:
                input_item_id = input_model.item(row, 1).data(Qt.DisplayRole)
                if input_item_id not in output_item_ids:
                    output_model.appendRow([input_item_name.clone(), input_model.item(row, 1).clone()])

            if input_item_name.checkState() == Qt.PartiallyChecked:
                self.clone_items_from_input_table(input_item_name)
                input_item_name.setCheckState(Qt.Unchecked)
            elif input_item_name.checkState() == Qt.Checked:
                self.clone_items_from_input_table(input_item_name)
                input_item_name.setCheckState(Qt.Unchecked)
                # input_item_name = input_model.takeItem(row, 0)
                input_model.removeRow(row)
                continue
            row += 1

        row = 0

        while row < output_model.rowCount():
            output_item_name = output_model.item(row, 0)
            self.iterate_output_category_tree_and_insert(output_item_name)
            output_item_name.setCheckState(Qt.Unchecked)
            row += 1

        # pprint.pp(f"output_items: {selected_items}")
        output_category_tree_view.resizeColumnToContents(0)
        print("The process of moving items has been completed.")
        self.populate_input_products_table()
        self.refresh_products_tables()

    def clone_items_from_input_table(self, input_item: QStandardItem):
        check_state: Qt.CheckState = input_item.checkState()
        if check_state != Qt.Unchecked:
            # TODO: make an optimization here
            clone_name_item = QStandardItem(input_item)
            clone_name_item.setCheckable(True)
            clone_id_item = QStandardItem()
            id_text = input_item.index().siblingAtColumn(1).data(Qt.DisplayRole)
            clone_id_item.setText(id_text)
            clone_id_item.setCheckable(False)
            if input_item.hasChildren():
                row = 0
                while row < input_item.rowCount():
                    child = input_item.child(row)
                    clone_child_name, clone_child_id_item = self.clone_items_from_input_table(child)
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
        items_list = []
        for row in range(output_item_name.rowCount()):
            child_id = output_item_name.child(row, 1)
            items_list.append(child_id.data(Qt.DisplayRole))

        if output_text_id in self.cloned_parentid_items_dict:
            input_items_list = self.cloned_parentid_items_dict.pop(output_text_id)
            for cloned_item in input_items_list:
                cloned_name_item = cloned_item["name"].clone()
                cloned_id_item = cloned_item["id"].clone()
                cloned_name_item.setCheckState(Qt.Unchecked)
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
        self.populate_input_category_table()
        self.populate_input_categories_replacement_table()
        self.populate_input_products_replacement_table()

    def populate_input_products_replacement_table(self):
        for product_id, product_data in self.input_products_replacement_dict.items():
            product_id_item = QStandardItem()
            product_id_item.setData(product_id, Qt.DisplayRole)
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

        self.output_xml_tree: ElementTree = copy.deepcopy(self.input_xml_tree)

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
                                                    "category_id": category_id_item}
            product_name_item = self.create_product_name_item(offer_tag)
            self.input_products_replacement_dict[product_id] = product_name_item

    def get_category_ids_and_names_from_xml(self):
        category_elems = self.input_xml_tree.xpath("//category")
        for category in category_elems:
            category_id, category_name_item = self.create_category_item(category)
            self.categoryid_parent_ids_dict[category_id] = category.get("parentId")
            self.input_categories_dict[category_id] = category_name_item.data(Qt.DisplayRole)
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

    def get_products_description_ids(self, old_product_name) -> set[str]:
        product_ids = set()
        output_xml_tree = self.output_xml_tree
        offer_tags = output_xml_tree.xpath("//offer")
        for offer_tag in offer_tags:
            description_text = offer_tag.xpath("description")[0].text
            if description_text is not None and old_product_name in description_text:
                product_id = offer_tag.get("id").strip()
                product_ids.add(product_id)
        return product_ids

    @staticmethod
    def create_category_item(category):
        category_id = category.get("id").strip()
        category_name = category.text.strip()
        category_name_item: QStandardItem = QStandardItem()
        category_name_item.setCheckable(True)
        category_name_item.setData(category_name, Qt.DisplayRole)
        return category_id, category_name_item

    def populate_input_category_table(self):
        # create a method that builds a tree of categories and subcategories from self.input_categories_dict
        graph = nx.DiGraph()
        parents_list = []
        for child_id, parent_id in self.categoryid_parent_ids_dict.items():
            if parent_id is None:
                graph.add_node(child_id)
                parents_list.append(child_id)
                self.parentid_childid_dict[child_id] = []
            else:
                if parent_id not in self.parentid_childid_dict:
                    self.parentid_childid_dict[parent_id] = []
                self.parentid_childid_dict[parent_id].append(child_id)
                graph.add_node(parent_id)
                graph.add_node(child_id)
                graph.add_edge(parent_id, child_id)

        for parent_id in parents_list:
            input_item_name = self.input_categories_dict[parent_id]
            input_item = QStandardItem(input_item_name)
            input_item.setCheckable(True)
            self.input_category_model.appendRow([input_item, QStandardItem(parent_id)])
            self.dfs(graph, parent_id, input_item)
        self.input_category_tree_view.resizeColumnToContents(0)
        self.input_category_names_table_view.resizeColumnToContents(0)

    def dfs(self, graph, child_id, parent_item, indent=0):
        print(" " * indent, parent_item.data(Qt.DisplayRole))
        for child_id in graph.neighbors(child_id):
            item = self.input_categories_dict[child_id]
            item = QStandardItem(item)
            item.setCheckable(True)
            parent_item.appendRow([item, QStandardItem(child_id)])
            self.dfs(graph, child_id, item, indent + 2)

    def get_products_names_ids(self, old_product_name):
        product_ids_names = set()
        for product_id, product_name in self.input_products_dict.items():
            if old_product_name in product_name["product_name"].data(Qt.DisplayRole):
                product_ids_names.add(product_id)
        return product_ids_names

# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainwindow.ui'
##
## Created by: Qt User Interface Compiler version 6.6.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QComboBox, QDoubleSpinBox, QGroupBox,
    QHBoxLayout, QHeaderView, QLabel, QLineEdit,
    QListView, QMainWindow, QMenu, QMenuBar,
    QPushButton, QScrollArea, QSizePolicy, QSpinBox,
    QStatusBar, QTabWidget, QTableView, QVBoxLayout,
    QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(820, 719)
        MainWindow.setLayoutDirection(Qt.LeftToRight)
        self.open_action = QAction(MainWindow)
        self.open_action.setObjectName(u"open_action")
        self.exit_action = QAction(MainWindow)
        self.exit_action.setObjectName(u"exit_action")
        self.action = QAction(MainWindow)
        self.action.setObjectName(u"action")
        self.action_2 = QAction(MainWindow)
        self.action_2.setObjectName(u"action_2")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout_20 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_20.setObjectName(u"verticalLayout_20")
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.verticalLayout_11 = QVBoxLayout(self.tab)
        self.verticalLayout_11.setObjectName(u"verticalLayout_11")
        self.groupBox_4 = QGroupBox(self.tab)
        self.groupBox_4.setObjectName(u"groupBox_4")
        self.verticalLayout_3 = QVBoxLayout(self.groupBox_4)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label_3 = QLabel(self.groupBox_4)
        self.label_3.setObjectName(u"label_3")

        self.horizontalLayout_2.addWidget(self.label_3)

        self.search_src_category_line_edit = QLineEdit(self.groupBox_4)
        self.search_src_category_line_edit.setObjectName(u"search_src_category_line_edit")

        self.horizontalLayout_2.addWidget(self.search_src_category_line_edit)


        self.verticalLayout_3.addLayout(self.horizontalLayout_2)

        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.check_all_source_categories_push_button = QPushButton(self.groupBox_4)
        self.check_all_source_categories_push_button.setObjectName(u"check_all_source_categories_push_button")

        self.horizontalLayout.addWidget(self.check_all_source_categories_push_button)

        self.uncheck_all_source_categories_push_button = QPushButton(self.groupBox_4)
        self.uncheck_all_source_categories_push_button.setObjectName(u"uncheck_all_source_categories_push_button")

        self.horizontalLayout.addWidget(self.uncheck_all_source_categories_push_button)

        self.add_cat_push_button = QPushButton(self.groupBox_4)
        self.add_cat_push_button.setObjectName(u"add_cat_push_button")

        self.horizontalLayout.addWidget(self.add_cat_push_button)


        self.verticalLayout_4.addLayout(self.horizontalLayout)

        self.source_category_table_view = QTableView(self.groupBox_4)
        self.source_category_table_view.setObjectName(u"source_category_table_view")

        self.verticalLayout_4.addWidget(self.source_category_table_view)


        self.verticalLayout_3.addLayout(self.verticalLayout_4)


        self.verticalLayout_11.addWidget(self.groupBox_4)

        self.groupBox_3 = QGroupBox(self.tab)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.verticalLayout_7 = QVBoxLayout(self.groupBox_3)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.horizontalLayout_14 = QHBoxLayout()
        self.horizontalLayout_14.setObjectName(u"horizontalLayout_14")
        self.label_13 = QLabel(self.groupBox_3)
        self.label_13.setObjectName(u"label_13")

        self.horizontalLayout_14.addWidget(self.label_13)

        self.search_fin_category_line_edit = QLineEdit(self.groupBox_3)
        self.search_fin_category_line_edit.setObjectName(u"search_fin_category_line_edit")

        self.horizontalLayout_14.addWidget(self.search_fin_category_line_edit)


        self.verticalLayout_7.addLayout(self.horizontalLayout_14)

        self.verticalLayout_5 = QVBoxLayout()
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.horizontalLayout_13 = QHBoxLayout()
        self.horizontalLayout_13.setObjectName(u"horizontalLayout_13")
        self.check_all_chosen_categories_push_button = QPushButton(self.groupBox_3)
        self.check_all_chosen_categories_push_button.setObjectName(u"check_all_chosen_categories_push_button")

        self.horizontalLayout_13.addWidget(self.check_all_chosen_categories_push_button)

        self.uncheck_all_chosen_categories_push_button = QPushButton(self.groupBox_3)
        self.uncheck_all_chosen_categories_push_button.setObjectName(u"uncheck_all_chosen_categories_push_button")

        self.horizontalLayout_13.addWidget(self.uncheck_all_chosen_categories_push_button)

        self.delete_cat_push_button = QPushButton(self.groupBox_3)
        self.delete_cat_push_button.setObjectName(u"delete_cat_push_button")

        self.horizontalLayout_13.addWidget(self.delete_cat_push_button)


        self.verticalLayout_5.addLayout(self.horizontalLayout_13)

        self.final_category_table_view = QTableView(self.groupBox_3)
        self.final_category_table_view.setObjectName(u"final_category_table_view")

        self.verticalLayout_5.addWidget(self.final_category_table_view)


        self.verticalLayout_7.addLayout(self.verticalLayout_5)


        self.verticalLayout_11.addWidget(self.groupBox_3)

        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.verticalLayout_10 = QVBoxLayout(self.tab_2)
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")
        self.scrollArea = QScrollArea(self.tab_2)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, -139, 757, 738))
        self.verticalLayout_12 = QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_12.setObjectName(u"verticalLayout_12")
        self.groupBox_5 = QGroupBox(self.scrollAreaWidgetContents)
        self.groupBox_5.setObjectName(u"groupBox_5")
        self.groupBox_5.setMinimumSize(QSize(0, 325))
        self.groupBox_5.setMaximumSize(QSize(16777215, 10000))
        self.verticalLayout_8 = QVBoxLayout(self.groupBox_5)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label_4 = QLabel(self.groupBox_5)
        self.label_4.setObjectName(u"label_4")

        self.horizontalLayout_3.addWidget(self.label_4)

        self.search_src_product_line_edit = QLineEdit(self.groupBox_5)
        self.search_src_product_line_edit.setObjectName(u"search_src_product_line_edit")

        self.horizontalLayout_3.addWidget(self.search_src_product_line_edit)


        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setSpacing(50)
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.pushButton_9 = QPushButton(self.groupBox_5)
        self.pushButton_9.setObjectName(u"pushButton_9")

        self.horizontalLayout_8.addWidget(self.pushButton_9)

        self.pushButton_7 = QPushButton(self.groupBox_5)
        self.pushButton_7.setObjectName(u"pushButton_7")

        self.horizontalLayout_8.addWidget(self.pushButton_7)

        self.add_prod_push_button = QPushButton(self.groupBox_5)
        self.add_prod_push_button.setObjectName(u"add_prod_push_button")

        self.horizontalLayout_8.addWidget(self.add_prod_push_button)


        self.verticalLayout.addLayout(self.horizontalLayout_8)

        self.source_products_table_view = QTableView(self.groupBox_5)
        self.source_products_table_view.setObjectName(u"source_products_table_view")
        self.source_products_table_view.setMaximumSize(QSize(16777215, 16777215))

        self.verticalLayout.addWidget(self.source_products_table_view)


        self.verticalLayout_8.addLayout(self.verticalLayout)


        self.verticalLayout_12.addWidget(self.groupBox_5)

        self.groupBox_6 = QGroupBox(self.scrollAreaWidgetContents)
        self.groupBox_6.setObjectName(u"groupBox_6")
        self.groupBox_6.setMinimumSize(QSize(0, 389))
        self.verticalLayout_9 = QVBoxLayout(self.groupBox_6)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.horizontalLayout_15 = QHBoxLayout()
        self.horizontalLayout_15.setObjectName(u"horizontalLayout_15")
        self.label_8 = QLabel(self.groupBox_6)
        self.label_8.setObjectName(u"label_8")

        self.horizontalLayout_15.addWidget(self.label_8)

        self.search_fin_product_line_edit = QLineEdit(self.groupBox_6)
        self.search_fin_product_line_edit.setObjectName(u"search_fin_product_line_edit")

        self.horizontalLayout_15.addWidget(self.search_fin_product_line_edit)


        self.verticalLayout_9.addLayout(self.horizontalLayout_15)

        self.verticalLayout_6 = QVBoxLayout()
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setSpacing(50)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.pushButton_10 = QPushButton(self.groupBox_6)
        self.pushButton_10.setObjectName(u"pushButton_10")

        self.horizontalLayout_7.addWidget(self.pushButton_10)

        self.pushButton_8 = QPushButton(self.groupBox_6)
        self.pushButton_8.setObjectName(u"pushButton_8")

        self.horizontalLayout_7.addWidget(self.pushButton_8)

        self.remove_prod_push_button = QPushButton(self.groupBox_6)
        self.remove_prod_push_button.setObjectName(u"remove_prod_push_button")

        self.horizontalLayout_7.addWidget(self.remove_prod_push_button)


        self.verticalLayout_6.addLayout(self.horizontalLayout_7)

        self.final_products_table_view = QTableView(self.groupBox_6)
        self.final_products_table_view.setObjectName(u"final_products_table_view")
        self.final_products_table_view.setMinimumSize(QSize(0, 1))
        self.final_products_table_view.setMaximumSize(QSize(16777215, 300))

        self.verticalLayout_6.addWidget(self.final_products_table_view)

        self.horizontalLayout_16 = QHBoxLayout()
        self.horizontalLayout_16.setObjectName(u"horizontalLayout_16")
        self.horizontalLayout_12 = QHBoxLayout()
        self.horizontalLayout_12.setSpacing(0)
        self.horizontalLayout_12.setObjectName(u"horizontalLayout_12")
        self.label_12 = QLabel(self.groupBox_6)
        self.label_12.setObjectName(u"label_12")
        self.label_12.setMinimumSize(QSize(76, 0))
        self.label_12.setMaximumSize(QSize(68, 16777215))

        self.horizontalLayout_12.addWidget(self.label_12)

        self.price_category_combo_box = QComboBox(self.groupBox_6)
        self.price_category_combo_box.addItem("")
        self.price_category_combo_box.addItem("")
        self.price_category_combo_box.setObjectName(u"price_category_combo_box")
        self.price_category_combo_box.setMaximumSize(QSize(94, 16777215))

        self.horizontalLayout_12.addWidget(self.price_category_combo_box)


        self.horizontalLayout_16.addLayout(self.horizontalLayout_12)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setSpacing(14)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.label_7 = QLabel(self.groupBox_6)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setMaximumSize(QSize(54, 16777215))

        self.horizontalLayout_6.addWidget(self.label_7)

        self.multiplier_double_spin_box = QDoubleSpinBox(self.groupBox_6)
        self.multiplier_double_spin_box.setObjectName(u"multiplier_double_spin_box")
        self.multiplier_double_spin_box.setMaximumSize(QSize(77, 16777215))

        self.horizontalLayout_6.addWidget(self.multiplier_double_spin_box)


        self.horizontalLayout_16.addLayout(self.horizontalLayout_6)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setSpacing(0)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.label_6 = QLabel(self.groupBox_6)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setMaximumSize(QSize(74, 16777215))

        self.horizontalLayout_4.addWidget(self.label_6)

        self.bottom_price_limit_spin_box = QSpinBox(self.groupBox_6)
        self.bottom_price_limit_spin_box.setObjectName(u"bottom_price_limit_spin_box")
        self.bottom_price_limit_spin_box.setMinimumSize(QSize(55, 0))
        self.bottom_price_limit_spin_box.setMaximumSize(QSize(69, 16777215))
        self.bottom_price_limit_spin_box.setMaximum(999999999)

        self.horizontalLayout_4.addWidget(self.bottom_price_limit_spin_box)


        self.horizontalLayout_16.addLayout(self.horizontalLayout_4)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.label_5 = QLabel(self.groupBox_6)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setMaximumSize(QSize(73, 16777215))

        self.horizontalLayout_5.addWidget(self.label_5)

        self.upper_price_limit_spin_box = QSpinBox(self.groupBox_6)
        self.upper_price_limit_spin_box.setObjectName(u"upper_price_limit_spin_box")
        self.upper_price_limit_spin_box.setMaximumSize(QSize(70, 16777215))
        self.upper_price_limit_spin_box.setMaximum(999999999)

        self.horizontalLayout_5.addWidget(self.upper_price_limit_spin_box)


        self.horizontalLayout_16.addLayout(self.horizontalLayout_5)

        self.apply_multiplier_push_button = QPushButton(self.groupBox_6)
        self.apply_multiplier_push_button.setObjectName(u"apply_multiplier_push_button")
        self.apply_multiplier_push_button.setMaximumSize(QSize(128, 16777215))

        self.horizontalLayout_16.addWidget(self.apply_multiplier_push_button)


        self.verticalLayout_6.addLayout(self.horizontalLayout_16)


        self.verticalLayout_9.addLayout(self.verticalLayout_6)


        self.verticalLayout_12.addWidget(self.groupBox_6)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.verticalLayout_10.addWidget(self.scrollArea)

        self.tabWidget.addTab(self.tab_2, "")
        self.tab_3 = QWidget()
        self.tab_3.setObjectName(u"tab_3")
        self.verticalLayout_19 = QVBoxLayout(self.tab_3)
        self.verticalLayout_19.setObjectName(u"verticalLayout_19")
        self.horizontalLayout_9 = QHBoxLayout()
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.groupBox = QGroupBox(self.tab_3)
        self.groupBox.setObjectName(u"groupBox")
        self.verticalLayout_18 = QVBoxLayout(self.groupBox)
        self.verticalLayout_18.setObjectName(u"verticalLayout_18")
        self.verticalLayout_15 = QVBoxLayout()
        self.verticalLayout_15.setObjectName(u"verticalLayout_15")
        self.verticalLayout_13 = QVBoxLayout()
        self.verticalLayout_13.setObjectName(u"verticalLayout_13")
        self.horizontalLayout_10 = QHBoxLayout()
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.label_10 = QLabel(self.groupBox)
        self.label_10.setObjectName(u"label_10")

        self.horizontalLayout_10.addWidget(self.label_10)

        self.search_product_line_edit_2 = QLineEdit(self.groupBox)
        self.search_product_line_edit_2.setObjectName(u"search_product_line_edit_2")

        self.horizontalLayout_10.addWidget(self.search_product_line_edit_2)


        self.verticalLayout_13.addLayout(self.horizontalLayout_10)

        self.listView = QListView(self.groupBox)
        self.listView.setObjectName(u"listView")

        self.verticalLayout_13.addWidget(self.listView)


        self.verticalLayout_15.addLayout(self.verticalLayout_13)

        self.horizontalLayout_17 = QHBoxLayout()
        self.horizontalLayout_17.setObjectName(u"horizontalLayout_17")
        self.pushButton = QPushButton(self.groupBox)
        self.pushButton.setObjectName(u"pushButton")

        self.horizontalLayout_17.addWidget(self.pushButton)


        self.verticalLayout_15.addLayout(self.horizontalLayout_17)


        self.verticalLayout_18.addLayout(self.verticalLayout_15)


        self.horizontalLayout_9.addWidget(self.groupBox)

        self.groupBox_2 = QGroupBox(self.tab_3)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.verticalLayout_17 = QVBoxLayout(self.groupBox_2)
        self.verticalLayout_17.setObjectName(u"verticalLayout_17")
        self.verticalLayout_16 = QVBoxLayout()
        self.verticalLayout_16.setObjectName(u"verticalLayout_16")
        self.verticalLayout_14 = QVBoxLayout()
        self.verticalLayout_14.setObjectName(u"verticalLayout_14")
        self.horizontalLayout_11 = QHBoxLayout()
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.label_11 = QLabel(self.groupBox_2)
        self.label_11.setObjectName(u"label_11")

        self.horizontalLayout_11.addWidget(self.label_11)

        self.search_product_line_edit_3 = QLineEdit(self.groupBox_2)
        self.search_product_line_edit_3.setObjectName(u"search_product_line_edit_3")

        self.horizontalLayout_11.addWidget(self.search_product_line_edit_3)


        self.verticalLayout_14.addLayout(self.horizontalLayout_11)

        self.listView_2 = QListView(self.groupBox_2)
        self.listView_2.setObjectName(u"listView_2")

        self.verticalLayout_14.addWidget(self.listView_2)


        self.verticalLayout_16.addLayout(self.verticalLayout_14)

        self.horizontalLayout_18 = QHBoxLayout()
        self.horizontalLayout_18.setObjectName(u"horizontalLayout_18")
        self.pushButton_11 = QPushButton(self.groupBox_2)
        self.pushButton_11.setObjectName(u"pushButton_11")

        self.horizontalLayout_18.addWidget(self.pushButton_11)


        self.verticalLayout_16.addLayout(self.horizontalLayout_18)


        self.verticalLayout_17.addLayout(self.verticalLayout_16)


        self.horizontalLayout_9.addWidget(self.groupBox_2)


        self.verticalLayout_19.addLayout(self.horizontalLayout_9)

        self.tabWidget.addTab(self.tab_3, "")

        self.verticalLayout_2.addWidget(self.tabWidget)

        self.horizontalLayout_19 = QHBoxLayout()
        self.horizontalLayout_19.setObjectName(u"horizontalLayout_19")
        self.get_new_xml_push_button = QPushButton(self.centralwidget)
        self.get_new_xml_push_button.setObjectName(u"get_new_xml_push_button")

        self.horizontalLayout_19.addWidget(self.get_new_xml_push_button)

        self.get_new_xml_push_button_2 = QPushButton(self.centralwidget)
        self.get_new_xml_push_button_2.setObjectName(u"get_new_xml_push_button_2")

        self.horizontalLayout_19.addWidget(self.get_new_xml_push_button_2)


        self.verticalLayout_2.addLayout(self.horizontalLayout_19)


        self.verticalLayout_20.addLayout(self.verticalLayout_2)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 820, 21))
        self.menu = QMenu(self.menubar)
        self.menu.setObjectName(u"menu")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menu.menuAction())
        self.menu.addAction(self.open_action)
        self.menu.addAction(self.action)
        self.menu.addAction(self.action_2)
        self.menu.addAction(self.exit_action)

        self.retranslateUi(MainWindow)
        self.exit_action.triggered.connect(MainWindow.close)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.open_action.setText(QCoreApplication.translate("MainWindow", u"\u0412\u0456\u0434\u043a\u0440\u0438\u0442\u0438 XML", None))
        self.exit_action.setText(QCoreApplication.translate("MainWindow", u"\u0412\u0438\u0445\u0456\u0434", None))
        self.action.setText(QCoreApplication.translate("MainWindow", u"\u0412\u0456\u0434\u043a\u0440\u0438\u0442\u0438 \u043f\u0440\u043e\u0435\u043a\u0442", None))
        self.action_2.setText(QCoreApplication.translate("MainWindow", u"\u0417\u0431\u0435\u0440\u0435\u0433\u0442\u0438 \u043f\u0440\u043e\u0435\u043a\u0442", None))
        self.groupBox_4.setTitle(QCoreApplication.translate("MainWindow", u"\u0412\u0441\u0456 \u043a\u0430\u0442\u0435\u0433\u043e\u0440\u0456\u0457 \u0442\u043e\u0432\u0430\u0440\u0456\u0432", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"\u041f\u043e\u0448\u0443\u043a:", None))
        self.check_all_source_categories_push_button.setText(QCoreApplication.translate("MainWindow", u"\u0412\u0438\u0431\u0440\u0430\u0442\u0438 \u0432\u0441\u0456", None))
        self.uncheck_all_source_categories_push_button.setText(QCoreApplication.translate("MainWindow", u"\u0417\u043d\u044f\u0442\u0438 \u0432\u0438\u0431\u0456\u0440 \u0437 \u0443\u0441\u0456\u0445", None))
        self.add_cat_push_button.setText(QCoreApplication.translate("MainWindow", u"\u0414\u043e\u0434\u0430\u0442\u0438 \u0434\u043e\n"
"XML", None))
        self.groupBox_3.setTitle(QCoreApplication.translate("MainWindow", u"\u041e\u0431\u0440\u0430\u043d\u0456 \u043a\u0430\u0442\u0435\u0433\u043e\u0440\u0456\u0457 \u0442\u043e\u0432\u0430\u0440\u0456\u0432 \u0434\u043b\u044f \u0432\u0438\u0432\u0430\u043d\u0442\u0430\u0436\u0435\u043d\u043d\u044f \u0434\u043e XML \u0444\u0430\u0439\u043b\u0443", None))
        self.label_13.setText(QCoreApplication.translate("MainWindow", u"\u041f\u043e\u0448\u0443\u043a:", None))
        self.check_all_chosen_categories_push_button.setText(QCoreApplication.translate("MainWindow", u"\u0412\u0438\u0431\u0440\u0430\u0442\u0438 \u0432\u0441\u0456", None))
        self.uncheck_all_chosen_categories_push_button.setText(QCoreApplication.translate("MainWindow", u"\u0417\u043d\u044f\u0442\u0438 \u0432\u0438\u0431\u0456\u0440 \u0437 \u0443\u0441\u0456\u0445", None))
        self.delete_cat_push_button.setText(QCoreApplication.translate("MainWindow", u"\u0423\u0431\u0440\u0430\u0442\u0438 \u0437\n"
"XML", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QCoreApplication.translate("MainWindow", u"\u041a\u0430\u0442\u0435\u0433\u043e\u0440\u0456\u0457", None))
        self.groupBox_5.setTitle(QCoreApplication.translate("MainWindow", u"\u0422\u043e\u0432\u0430\u0440\u0438 \u0437 \u043e\u0431\u0440\u0430\u043d\u0438\u0445 \u043a\u0430\u0442\u0435\u0433\u043e\u0440\u0456\u0439", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"\u041f\u043e\u0448\u0443\u043a:", None))
        self.pushButton_9.setText(QCoreApplication.translate("MainWindow", u"\u0412\u0438\u0431\u0440\u0430\u0442\u0438 \u0432\u0441\u0456", None))
        self.pushButton_7.setText(QCoreApplication.translate("MainWindow", u"\u0417\u043d\u044f\u0442\u0438 \u0432\u0438\u0431\u0456\u0440 \u0437 \u0443\u0441\u0456\u0445", None))
        self.add_prod_push_button.setText(QCoreApplication.translate("MainWindow", u"\u0414\u043e\u0434\u0430\u0442\u0438 \u0434\u043e\n"
"XML", None))
        self.groupBox_6.setTitle(QCoreApplication.translate("MainWindow", u"\u041e\u0431\u0440\u0430\u043d\u0456 \u0442\u043e\u0432\u0430\u0440\u0438 \u0434\u043b\u044f \u0432\u0438\u0432\u0430\u043d\u0442\u0430\u0436\u0435\u043d\u043d\u044f \u0432 XML \u0444\u0430\u0439\u043b", None))
        self.label_8.setText(QCoreApplication.translate("MainWindow", u"\u041f\u043e\u0448\u0443\u043a:", None))
        self.pushButton_10.setText(QCoreApplication.translate("MainWindow", u"\u0412\u0438\u0431\u0440\u0430\u0442\u0438 \u0432\u0441\u0456", None))
        self.pushButton_8.setText(QCoreApplication.translate("MainWindow", u"\u0417\u043d\u044f\u0442\u0438 \u0432\u0438\u0431\u0456\u0440 \u0437 \u0443\u0441\u0456\u0445", None))
        self.remove_prod_push_button.setText(QCoreApplication.translate("MainWindow", u"\u0423\u0431\u0440\u0430\u0442\u0438 \u0437\n"
"XML", None))
        self.label_12.setText(QCoreApplication.translate("MainWindow", u"\u041a\u0430\u0442\u0435\u0433\u043e\u0440\u0456\u044f \u0446\u0456\u043d", None))
        self.price_category_combo_box.setItemText(0, QCoreApplication.translate("MainWindow", u"\u041e\u043f\u0442\u043e\u0432\u0430 \u0426\u0456\u043d\u0430", None))
        self.price_category_combo_box.setItemText(1, QCoreApplication.translate("MainWindow", u"\u0414\u0440\u043e\u043f \u0426\u0456\u043d\u0430", None))

        self.label_7.setText(QCoreApplication.translate("MainWindow", u"\u041c\u043d\u043e\u0436\u043d\u0438\u043a", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"\u041d\u0438\u0436\u043d\u044f \u043c\u0435\u0436\u0430\n"
"(\u0432\u043a\u043b\u044e\u0447\u043d\u043e)", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"\u0412\u0435\u0440\u0445\u043d\u044f \u043c\u0435\u0436\u0430\n"
"(\u0432\u043a\u043b\u044e\u0447\u043d\u043e)", None))
        self.apply_multiplier_push_button.setText(QCoreApplication.translate("MainWindow", u"\u0417\u0430\u0441\u0442\u043e\u0441\u0443\u0432\u0430\u0442\u0438 \u043c\u043d\u043e\u0436\u043d\u0438\u043a", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QCoreApplication.translate("MainWindow", u"\u0422\u043e\u0432\u0430\u0440\u0438", None))
        self.groupBox.setTitle(QCoreApplication.translate("MainWindow", u"\u041a\u0430\u0442\u0435\u0433\u043e\u0440\u0456\u0457", None))
        self.label_10.setText(QCoreApplication.translate("MainWindow", u"\u041f\u043e\u0448\u0443\u043a:", None))
        self.pushButton.setText(QCoreApplication.translate("MainWindow", u"\u0417\u0430\u043c\u0456\u043d\u0438\u0442\u0438", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("MainWindow", u"\u0422\u043e\u0432\u0430\u0440\u0438", None))
        self.label_11.setText(QCoreApplication.translate("MainWindow", u"\u041f\u043e\u0448\u0443\u043a:", None))
        self.pushButton_11.setText(QCoreApplication.translate("MainWindow", u"\u0417\u0430\u043c\u0456\u043d\u0438\u0442\u0438", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), QCoreApplication.translate("MainWindow", u"\u0417\u0430\u043c\u0456\u043d\u0430 \u0441\u043b\u0456\u0432", None))
        self.get_new_xml_push_button.setText(QCoreApplication.translate("MainWindow", u"\u041e\u0442\u0440\u0438\u043c\u0430\u0442\u0438 XML", None))
        self.get_new_xml_push_button_2.setText(QCoreApplication.translate("MainWindow", u"\u041e\u0442\u0440\u0438\u043c\u0430\u0442\u0438 CSV", None))
        self.menu.setTitle(QCoreApplication.translate("MainWindow", u"\u0424\u0430\u0439\u043b", None))
    # retranslateUi


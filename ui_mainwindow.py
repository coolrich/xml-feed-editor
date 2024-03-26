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
    QPushButton, QSizePolicy, QSpinBox, QStatusBar,
    QTabWidget, QTableView, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(702, 384)
        MainWindow.setLayoutDirection(Qt.LeftToRight)
        self.open_action = QAction(MainWindow)
        self.open_action.setObjectName(u"open_action")
        self.exit_action = QAction(MainWindow)
        self.exit_action.setObjectName(u"exit_action")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setGeometry(QRect(10, 10, 681, 281))
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.label_2 = QLabel(self.tab)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(350, -2, 251, 41))
        self.widget = QWidget(self.tab)
        self.widget.setObjectName(u"widget")
        self.widget.setGeometry(QRect(4, 78, 601, 111))
        self.horizontalLayout = QHBoxLayout(self.widget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.source_category_table_view = QTableView(self.widget)
        self.source_category_table_view.setObjectName(u"source_category_table_view")

        self.horizontalLayout.addWidget(self.source_category_table_view)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.add_cat_push_button = QPushButton(self.widget)
        self.add_cat_push_button.setObjectName(u"add_cat_push_button")

        self.verticalLayout.addWidget(self.add_cat_push_button)

        self.delete_cat_push_button = QPushButton(self.widget)
        self.delete_cat_push_button.setObjectName(u"delete_cat_push_button")

        self.verticalLayout.addWidget(self.delete_cat_push_button)


        self.horizontalLayout.addLayout(self.verticalLayout)

        self.final_category_table_view = QTableView(self.widget)
        self.final_category_table_view.setObjectName(u"final_category_table_view")

        self.horizontalLayout.addWidget(self.final_category_table_view)

        self.label = QLabel(self.tab)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(6, 2, 111, 16))
        self.pushButton_3 = QPushButton(self.tab)
        self.pushButton_3.setObjectName(u"pushButton_3")
        self.pushButton_3.setGeometry(QRect(10, 50, 70, 23))
        self.pushButton_4 = QPushButton(self.tab)
        self.pushButton_4.setObjectName(u"pushButton_4")
        self.pushButton_4.setGeometry(QRect(90, 50, 121, 23))
        self.pushButton_5 = QPushButton(self.tab)
        self.pushButton_5.setObjectName(u"pushButton_5")
        self.pushButton_5.setGeometry(QRect(430, 50, 121, 23))
        self.pushButton_6 = QPushButton(self.tab)
        self.pushButton_6.setObjectName(u"pushButton_6")
        self.pushButton_6.setGeometry(QRect(350, 50, 70, 23))
        self.widget1 = QWidget(self.tab)
        self.widget1.setObjectName(u"widget1")
        self.widget1.setGeometry(QRect(4, 20, 251, 22))
        self.horizontalLayout_2 = QHBoxLayout(self.widget1)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.label_3 = QLabel(self.widget1)
        self.label_3.setObjectName(u"label_3")

        self.horizontalLayout_2.addWidget(self.label_3)

        self.search_category_line_edit = QLineEdit(self.widget1)
        self.search_category_line_edit.setObjectName(u"search_category_line_edit")

        self.horizontalLayout_2.addWidget(self.search_category_line_edit)

        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.label_8 = QLabel(self.tab_2)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setGeometry(QRect(10, -1, 251, 16))
        self.label_9 = QLabel(self.tab_2)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setGeometry(QRect(380, -7, 251, 41))
        self.widget2 = QWidget(self.tab_2)
        self.widget2.setObjectName(u"widget2")
        self.widget2.setGeometry(QRect(10, 199, 651, 30))
        self.horizontalLayout_7 = QHBoxLayout(self.widget2)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.horizontalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_12 = QHBoxLayout()
        self.horizontalLayout_12.setSpacing(0)
        self.horizontalLayout_12.setObjectName(u"horizontalLayout_12")
        self.label_12 = QLabel(self.widget2)
        self.label_12.setObjectName(u"label_12")
        self.label_12.setMinimumSize(QSize(76, 0))
        self.label_12.setMaximumSize(QSize(16777215, 16777215))

        self.horizontalLayout_12.addWidget(self.label_12)

        self.comboBox = QComboBox(self.widget2)
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.setObjectName(u"comboBox")

        self.horizontalLayout_12.addWidget(self.comboBox)


        self.horizontalLayout_4.addLayout(self.horizontalLayout_12)

        self.label_6 = QLabel(self.widget2)
        self.label_6.setObjectName(u"label_6")

        self.horizontalLayout_4.addWidget(self.label_6)

        self.spinBox = QSpinBox(self.widget2)
        self.spinBox.setObjectName(u"spinBox")
        self.spinBox.setMinimumSize(QSize(55, 0))
        self.spinBox.setMaximumSize(QSize(55, 16777215))

        self.horizontalLayout_4.addWidget(self.spinBox)


        self.horizontalLayout_7.addLayout(self.horizontalLayout_4)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.label_5 = QLabel(self.widget2)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setMaximumSize(QSize(68, 16777215))

        self.horizontalLayout_5.addWidget(self.label_5)

        self.spinBox_2 = QSpinBox(self.widget2)
        self.spinBox_2.setObjectName(u"spinBox_2")
        self.spinBox_2.setMaximumSize(QSize(55, 16777215))

        self.horizontalLayout_5.addWidget(self.spinBox_2)


        self.horizontalLayout_7.addLayout(self.horizontalLayout_5)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setSpacing(0)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.label_7 = QLabel(self.widget2)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setMaximumSize(QSize(49, 16777215))

        self.horizontalLayout_6.addWidget(self.label_7)

        self.doubleSpinBox = QDoubleSpinBox(self.widget2)
        self.doubleSpinBox.setObjectName(u"doubleSpinBox")
        self.doubleSpinBox.setMaximumSize(QSize(42, 16777215))

        self.horizontalLayout_6.addWidget(self.doubleSpinBox)


        self.horizontalLayout_7.addLayout(self.horizontalLayout_6)

        self.pushButton_2 = QPushButton(self.widget2)
        self.pushButton_2.setObjectName(u"pushButton_2")
        self.pushButton_2.setMaximumSize(QSize(128, 16777215))

        self.horizontalLayout_7.addWidget(self.pushButton_2)

        self.pushButton_7 = QPushButton(self.tab_2)
        self.pushButton_7.setObjectName(u"pushButton_7")
        self.pushButton_7.setGeometry(QRect(90, 49, 121, 23))
        self.pushButton_8 = QPushButton(self.tab_2)
        self.pushButton_8.setObjectName(u"pushButton_8")
        self.pushButton_8.setGeometry(QRect(460, 49, 121, 23))
        self.pushButton_9 = QPushButton(self.tab_2)
        self.pushButton_9.setObjectName(u"pushButton_9")
        self.pushButton_9.setGeometry(QRect(10, 49, 70, 23))
        self.pushButton_10 = QPushButton(self.tab_2)
        self.pushButton_10.setObjectName(u"pushButton_10")
        self.pushButton_10.setGeometry(QRect(380, 49, 70, 23))
        self.widget3 = QWidget(self.tab_2)
        self.widget3.setObjectName(u"widget3")
        self.widget3.setGeometry(QRect(10, 23, 251, 22))
        self.horizontalLayout_3 = QHBoxLayout(self.widget3)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.label_4 = QLabel(self.widget3)
        self.label_4.setObjectName(u"label_4")

        self.horizontalLayout_3.addWidget(self.label_4)

        self.search_product_line_edit = QLineEdit(self.widget3)
        self.search_product_line_edit.setObjectName(u"search_product_line_edit")

        self.horizontalLayout_3.addWidget(self.search_product_line_edit)

        self.widget4 = QWidget(self.tab_2)
        self.widget4.setObjectName(u"widget4")
        self.widget4.setGeometry(QRect(10, 79, 651, 111))
        self.horizontalLayout_8 = QHBoxLayout(self.widget4)
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.horizontalLayout_8.setContentsMargins(0, 0, 0, 0)
        self.source_products_table_view = QTableView(self.widget4)
        self.source_products_table_view.setObjectName(u"source_products_table_view")

        self.horizontalLayout_8.addWidget(self.source_products_table_view)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.add_cat_push_button_2 = QPushButton(self.widget4)
        self.add_cat_push_button_2.setObjectName(u"add_cat_push_button_2")

        self.verticalLayout_2.addWidget(self.add_cat_push_button_2)

        self.delete_cat_push_button_2 = QPushButton(self.widget4)
        self.delete_cat_push_button_2.setObjectName(u"delete_cat_push_button_2")

        self.verticalLayout_2.addWidget(self.delete_cat_push_button_2)


        self.horizontalLayout_8.addLayout(self.verticalLayout_2)

        self.final_products_table_view = QTableView(self.widget4)
        self.final_products_table_view.setObjectName(u"final_products_table_view")

        self.horizontalLayout_8.addWidget(self.final_products_table_view)

        self.tabWidget.addTab(self.tab_2, "")
        self.tab_3 = QWidget()
        self.tab_3.setObjectName(u"tab_3")
        self.widget5 = QWidget(self.tab_3)
        self.widget5.setObjectName(u"widget5")
        self.widget5.setGeometry(QRect(11, 10, 651, 231))
        self.horizontalLayout_9 = QHBoxLayout(self.widget5)
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.horizontalLayout_9.setContentsMargins(0, 0, 0, 0)
        self.groupBox = QGroupBox(self.widget5)
        self.groupBox.setObjectName(u"groupBox")
        self.layoutWidget = QWidget(self.groupBox)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.layoutWidget.setGeometry(QRect(10, 20, 251, 22))
        self.horizontalLayout_10 = QHBoxLayout(self.layoutWidget)
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.horizontalLayout_10.setContentsMargins(0, 0, 0, 0)
        self.label_10 = QLabel(self.layoutWidget)
        self.label_10.setObjectName(u"label_10")

        self.horizontalLayout_10.addWidget(self.label_10)

        self.search_product_line_edit_2 = QLineEdit(self.layoutWidget)
        self.search_product_line_edit_2.setObjectName(u"search_product_line_edit_2")

        self.horizontalLayout_10.addWidget(self.search_product_line_edit_2)

        self.listView = QListView(self.groupBox)
        self.listView.setObjectName(u"listView")
        self.listView.setGeometry(QRect(10, 50, 256, 131))

        self.horizontalLayout_9.addWidget(self.groupBox)

        self.groupBox_2 = QGroupBox(self.widget5)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.layoutWidget_2 = QWidget(self.groupBox_2)
        self.layoutWidget_2.setObjectName(u"layoutWidget_2")
        self.layoutWidget_2.setGeometry(QRect(10, 20, 251, 22))
        self.horizontalLayout_11 = QHBoxLayout(self.layoutWidget_2)
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.horizontalLayout_11.setContentsMargins(0, 0, 0, 0)
        self.label_11 = QLabel(self.layoutWidget_2)
        self.label_11.setObjectName(u"label_11")

        self.horizontalLayout_11.addWidget(self.label_11)

        self.search_product_line_edit_3 = QLineEdit(self.layoutWidget_2)
        self.search_product_line_edit_3.setObjectName(u"search_product_line_edit_3")

        self.horizontalLayout_11.addWidget(self.search_product_line_edit_3)

        self.listView_2 = QListView(self.groupBox_2)
        self.listView_2.setObjectName(u"listView_2")
        self.listView_2.setGeometry(QRect(10, 50, 256, 131))

        self.horizontalLayout_9.addWidget(self.groupBox_2)

        self.tabWidget.addTab(self.tab_3, "")
        self.pushButton = QPushButton(self.centralwidget)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setGeometry(QRect(600, 300, 91, 23))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 702, 21))
        self.menu = QMenu(self.menubar)
        self.menu.setObjectName(u"menu")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menu.menuAction())
        self.menu.addAction(self.open_action)
        self.menu.addAction(self.exit_action)

        self.retranslateUi(MainWindow)
        self.exit_action.triggered.connect(MainWindow.close)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.open_action.setText(QCoreApplication.translate("MainWindow", u"\u0412\u0456\u0434\u043a\u0440\u0438\u0442\u0438", None))
        self.exit_action.setText(QCoreApplication.translate("MainWindow", u"\u0412\u0438\u0445\u0456\u0434", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"\u041e\u0431\u0440\u0430\u043d\u0456 \u043a\u0430\u0442\u0435\u0433\u043e\u0440\u0456\u0457 \u0442\u043e\u0432\u0430\u0440\u0456\u0432 \u0434\u043b\u044f \u0432\u0438\u0432\u0430\u043d\u0442\u0430\u0436\u0435\u043d\u043d\u044f\n"
"\u0432 XML \u0444\u0430\u0439\u043b", None))
        self.add_cat_push_button.setText(QCoreApplication.translate("MainWindow", u"\u0414\u043e\u0434\u0430\u0442\u0438 \u0434\u043e\n"
"XML", None))
        self.delete_cat_push_button.setText(QCoreApplication.translate("MainWindow", u"\u0423\u0431\u0440\u0430\u0442\u0438 \u0437\n"
"XML", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"\u0412\u0441\u0456 \u043a\u0430\u0442\u0435\u0433\u043e\u0440\u0456\u0457 \u0442\u043e\u0432\u0430\u0440\u0456\u0432", None))
        self.pushButton_3.setText(QCoreApplication.translate("MainWindow", u"\u0412\u0438\u0431\u0440\u0430\u0442\u0438 \u0432\u0441\u0456", None))
        self.pushButton_4.setText(QCoreApplication.translate("MainWindow", u"\u0417\u043d\u044f\u0442\u0438 \u0432\u0438\u0431\u0456\u0440 \u0437 \u0443\u0441\u0456\u0445", None))
        self.pushButton_5.setText(QCoreApplication.translate("MainWindow", u"\u0417\u043d\u044f\u0442\u0438 \u0432\u0438\u0431\u0456\u0440 \u0437 \u0443\u0441\u0456\u0445", None))
        self.pushButton_6.setText(QCoreApplication.translate("MainWindow", u"\u0412\u0438\u0431\u0440\u0430\u0442\u0438 \u0432\u0441\u0456", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"\u041f\u043e\u0448\u0443\u043a:", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QCoreApplication.translate("MainWindow", u"\u041a\u0430\u0442\u0435\u0433\u043e\u0440\u0456\u0457", None))
        self.label_8.setText(QCoreApplication.translate("MainWindow", u"\u0422\u043e\u0432\u0430\u0440\u0438 \u0437 \u043e\u0431\u0440\u0430\u043d\u0438\u0445 \u043a\u0430\u0442\u0435\u0433\u043e\u0440\u0456\u0439", None))
        self.label_9.setText(QCoreApplication.translate("MainWindow", u"\u041e\u0431\u0440\u0430\u043d\u0456 \u0442\u043e\u0432\u0430\u0440\u0438 \u0434\u043b\u044f \u0432\u0438\u0432\u0430\u043d\u0442\u0430\u0436\u0435\u043d\u043d\u044f\n"
"\u0432 XML \u0444\u0430\u0439\u043b", None))
        self.label_12.setText(QCoreApplication.translate("MainWindow", u"\u041a\u0430\u0442\u0435\u0433\u043e\u0440\u0456\u044f \u0446\u0456\u043d", None))
        self.comboBox.setItemText(0, QCoreApplication.translate("MainWindow", u"\u0414\u0440\u043e\u043f", None))
        self.comboBox.setItemText(1, QCoreApplication.translate("MainWindow", u"\u041e\u043f\u0442", None))

        self.comboBox.setCurrentText(QCoreApplication.translate("MainWindow", u"\u0414\u0440\u043e\u043f", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"\u041d\u0438\u0436\u043d\u044f \u043c\u0435\u0436\u0430\n"
"(\u0432\u043a\u043b\u044e\u0447\u043d\u043e)", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"\u0412\u0435\u0440\u0445\u043d\u044f \u043c\u0435\u0436\u0430\n"
"(\u0432\u043a\u043b\u044e\u0447\u043d\u043e)", None))
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"\u041c\u043d\u043e\u0436\u043d\u0438\u043a", None))
        self.pushButton_2.setText(QCoreApplication.translate("MainWindow", u"\u0417\u0430\u0441\u0442\u043e\u0441\u0443\u0432\u0430\u0442\u0438 \u043c\u043d\u043e\u0436\u043d\u0438\u043a", None))
        self.pushButton_7.setText(QCoreApplication.translate("MainWindow", u"\u0417\u043d\u044f\u0442\u0438 \u0432\u0438\u0431\u0456\u0440 \u0437 \u0443\u0441\u0456\u0445", None))
        self.pushButton_8.setText(QCoreApplication.translate("MainWindow", u"\u0417\u043d\u044f\u0442\u0438 \u0432\u0438\u0431\u0456\u0440 \u0437 \u0443\u0441\u0456\u0445", None))
        self.pushButton_9.setText(QCoreApplication.translate("MainWindow", u"\u0412\u0438\u0431\u0440\u0430\u0442\u0438 \u0432\u0441\u0456", None))
        self.pushButton_10.setText(QCoreApplication.translate("MainWindow", u"\u0412\u0438\u0431\u0440\u0430\u0442\u0438 \u0432\u0441\u0456", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"\u041f\u043e\u0448\u0443\u043a:", None))
        self.add_cat_push_button_2.setText(QCoreApplication.translate("MainWindow", u"\u0414\u043e\u0434\u0430\u0442\u0438 \u0434\u043e\n"
"XML", None))
        self.delete_cat_push_button_2.setText(QCoreApplication.translate("MainWindow", u"\u0423\u0431\u0440\u0430\u0442\u0438 \u0437\n"
"XML", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QCoreApplication.translate("MainWindow", u"\u0422\u043e\u0432\u0430\u0440\u0438", None))
        self.groupBox.setTitle(QCoreApplication.translate("MainWindow", u"\u041a\u0430\u0442\u0435\u0433\u043e\u0440\u0456\u0457", None))
        self.label_10.setText(QCoreApplication.translate("MainWindow", u"\u041f\u043e\u0448\u0443\u043a:", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("MainWindow", u"\u0422\u043e\u0432\u0430\u0440\u0438", None))
        self.label_11.setText(QCoreApplication.translate("MainWindow", u"\u041f\u043e\u0448\u0443\u043a:", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), QCoreApplication.translate("MainWindow", u"\u0417\u0430\u043c\u0456\u043d\u0430 \u0441\u043b\u0456\u0432", None))
        self.pushButton.setText(QCoreApplication.translate("MainWindow", u"\u041e\u0442\u0440\u0438\u043c\u0430\u0442\u0438 XML", None))
        self.menu.setTitle(QCoreApplication.translate("MainWindow", u"\u0424\u0430\u0439\u043b", None))
    # retranslateUi


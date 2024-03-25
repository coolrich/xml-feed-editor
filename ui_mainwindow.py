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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QHeaderView, QLabel,
    QLineEdit, QMainWindow, QMenu, QMenuBar,
    QPushButton, QSizePolicy, QStatusBar, QTableView,
    QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(666, 253)
        self.open_action = QAction(MainWindow)
        self.open_action.setObjectName(u"open_action")
        self.exit_action = QAction(MainWindow)
        self.exit_action.setObjectName(u"exit_action")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.pushButton = QPushButton(self.centralwidget)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setGeometry(QRect(10, 180, 91, 23))
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(10, 0, 111, 16))
        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(356, 0, 100, 16))
        self.search_line_edit = QLineEdit(self.centralwidget)
        self.search_line_edit.setObjectName(u"search_line_edit")
        self.search_line_edit.setGeometry(QRect(60, 37, 201, 20))
        self.label_3 = QLabel(self.centralwidget)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(14, 40, 47, 13))
        self.widget = QWidget(self.centralwidget)
        self.widget.setObjectName(u"widget")
        self.widget.setGeometry(QRect(10, 60, 601, 111))
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

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 666, 21))
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

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.open_action.setText(QCoreApplication.translate("MainWindow", u"\u0412\u0456\u0434\u043a\u0440\u0438\u0442\u0438", None))
        self.exit_action.setText(QCoreApplication.translate("MainWindow", u"\u0412\u0438\u0445\u0456\u0434", None))
        self.pushButton.setText(QCoreApplication.translate("MainWindow", u"\u041e\u0442\u0440\u0438\u043c\u0430\u0442\u0438 XML", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"\u041f\u043e\u0447\u0430\u0442\u043a\u043e\u0432\u0438\u0439 \u0441\u043f\u0438\u0441\u043e\u043a", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"\u041a\u0456\u043d\u0446\u0435\u0432\u0438\u0439 \u0441\u043f\u0438\u0441\u043e\u043a", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"\u041f\u043e\u0448\u0443\u043a:", None))
        self.add_cat_push_button.setText(QCoreApplication.translate("MainWindow", u"\u0414\u043e\u0434\u0430\u0442\u0438 \u0434\u043e\n"
"XML", None))
        self.delete_cat_push_button.setText(QCoreApplication.translate("MainWindow", u"\u0423\u0431\u0440\u0430\u0442\u0438 \u0437\n"
"XML", None))
        self.menu.setTitle(QCoreApplication.translate("MainWindow", u"\u0424\u0430\u0439\u043b", None))
    # retranslateUi


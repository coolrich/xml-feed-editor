# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'download_xml_window.ui'
##
## Created by: Qt User Interface Compiler version 6.6.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QSizePolicy, QSpinBox, QVBoxLayout,
    QWidget)

class Ui_DownloadXmlWindow(object):
    def setupUi(self, DownloadXmlWindow):
        if not DownloadXmlWindow.objectName():
            DownloadXmlWindow.setObjectName(u"DownloadXmlWindow")
        DownloadXmlWindow.setWindowModality(Qt.ApplicationModal)
        DownloadXmlWindow.setEnabled(True)
        DownloadXmlWindow.resize(411, 134)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(DownloadXmlWindow.sizePolicy().hasHeightForWidth())
        DownloadXmlWindow.setSizePolicy(sizePolicy)
        DownloadXmlWindow.setMinimumSize(QSize(411, 134))
        DownloadXmlWindow.setMaximumSize(QSize(411, 134))
        self.horizontalLayout = QHBoxLayout(DownloadXmlWindow)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label = QLabel(DownloadXmlWindow)
        self.label.setObjectName(u"label")

        self.horizontalLayout_2.addWidget(self.label)

        self.url_line_edit = QLineEdit(DownloadXmlWindow)
        self.url_line_edit.setObjectName(u"url_line_edit")

        self.horizontalLayout_2.addWidget(self.url_line_edit)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label_2 = QLabel(DownloadXmlWindow)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout_3.addWidget(self.label_2)

        self.timeout_spin_box = QSpinBox(DownloadXmlWindow)
        self.timeout_spin_box.setObjectName(u"timeout_spin_box")
        self.timeout_spin_box.setValue(5)

        self.horizontalLayout_3.addWidget(self.timeout_spin_box)


        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.download_xml_push_button = QPushButton(DownloadXmlWindow)
        self.download_xml_push_button.setObjectName(u"download_xml_push_button")

        self.verticalLayout.addWidget(self.download_xml_push_button)


        self.horizontalLayout.addLayout(self.verticalLayout)


        self.retranslateUi(DownloadXmlWindow)

        QMetaObject.connectSlotsByName(DownloadXmlWindow)
    # setupUi

    def retranslateUi(self, DownloadXmlWindow):
        DownloadXmlWindow.setWindowTitle(QCoreApplication.translate("DownloadXmlWindow", u"\u0417\u0430\u0432\u0430\u043d\u0442\u0430\u0436\u0438\u0442\u0438 xml", None))
        self.label.setText(QCoreApplication.translate("DownloadXmlWindow", u"URL \u043f\u043e\u0441\u0438\u043b\u0430\u043d\u043d\u044f", None))
        self.label_2.setText(QCoreApplication.translate("DownloadXmlWindow", u"\u041c\u0430\u043a\u0441\u0438\u043c\u0430\u043b\u044c\u043d\u0438\u0439 \u0447\u0430\u0441 \u043e\u0447\u0456\u043a\u0443\u0432\u0430\u043d\u043d\u044f \u0437\u0430\u0432\u0430\u043d\u0442\u0430\u0436\u0435\u043d\u043d\u044f (\u0445\u0432)", None))
        self.download_xml_push_button.setText(QCoreApplication.translate("DownloadXmlWindow", u"\u0417\u0430\u0432\u0430\u043d\u0442\u0430\u0436\u0438\u0442\u0438", None))
    # retranslateUi


# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'section.ui'
##
## Created by: Qt User Interface Compiler version 6.5.0
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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLabel, QPushButton,
    QSizePolicy, QTextEdit, QVBoxLayout, QWidget)

class Ui_SectionWidget(object):
    def setupUi(self, SectionWidget):
        if not SectionWidget.objectName():
            SectionWidget.setObjectName(u"SectionWidget")
        SectionWidget.resize(513, 378)
        self.horizontalLayout_2 = QHBoxLayout(SectionWidget)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.label = QLabel(SectionWidget)
        self.label.setObjectName(u"label")

        self.verticalLayout_2.addWidget(self.label)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.text_area = QTextEdit(SectionWidget)
        self.text_area.setObjectName(u"text_area")

        self.verticalLayout.addWidget(self.text_area)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.edit_button = QPushButton(SectionWidget)
        self.edit_button.setObjectName(u"edit_button")

        self.horizontalLayout.addWidget(self.edit_button)

        self.confirm_button = QPushButton(SectionWidget)
        self.confirm_button.setObjectName(u"confirm_button")

        self.horizontalLayout.addWidget(self.confirm_button)


        self.verticalLayout.addLayout(self.horizontalLayout)


        self.verticalLayout_2.addLayout(self.verticalLayout)


        self.horizontalLayout_2.addLayout(self.verticalLayout_2)


        self.retranslateUi(SectionWidget)

        QMetaObject.connectSlotsByName(SectionWidget)
    # setupUi

    def retranslateUi(self, SectionWidget):
        SectionWidget.setWindowTitle(QCoreApplication.translate("SectionWidget", u"Form", None))
        self.label.setText(QCoreApplication.translate("SectionWidget", u"Section: ", None))
        self.edit_button.setText(QCoreApplication.translate("SectionWidget", u"Edit", None))
        self.confirm_button.setText(QCoreApplication.translate("SectionWidget", u"Confirm", None))
    # retranslateUi


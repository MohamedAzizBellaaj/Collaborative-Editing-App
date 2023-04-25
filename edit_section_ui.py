# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'edit_section.ui'
##
## Created by: Qt User Interface Compiler version 6.5.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (
    QCoreApplication,
    QDate,
    QDateTime,
    QLocale,
    QMetaObject,
    QObject,
    QPoint,
    QRect,
    QSize,
    Qt,
    QTime,
    QUrl,
)
from PySide6.QtGui import (
    QBrush,
    QColor,
    QConicalGradient,
    QCursor,
    QFont,
    QFontDatabase,
    QGradient,
    QIcon,
    QImage,
    QKeySequence,
    QLinearGradient,
    QPainter,
    QPalette,
    QPixmap,
    QRadialGradient,
    QTransform,
)
from PySide6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QSizePolicy,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)


class Ui_EditSectionWidget(object):
    def setupUi(self, EditSectionWidget):
        if not EditSectionWidget.objectName():
            EditSectionWidget.setObjectName(u"EditSectionWidget")
        EditSectionWidget.resize(513, 378)
        self.horizontalLayout_2 = QHBoxLayout(EditSectionWidget)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.label = QLabel(EditSectionWidget)
        self.label.setObjectName(u"label")

        self.verticalLayout_2.addWidget(self.label)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.text_area = QTextEdit(EditSectionWidget)
        self.text_area.setObjectName(u"text_area")

        self.verticalLayout.addWidget(self.text_area)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.edit_button = QPushButton(EditSectionWidget)
        self.edit_button.setObjectName(u"edit_button")

        self.horizontalLayout.addWidget(self.edit_button)

        self.confirm_button = QPushButton(EditSectionWidget)
        self.confirm_button.setObjectName(u"confirm_button")

        self.horizontalLayout.addWidget(self.confirm_button)


        self.verticalLayout.addLayout(self.horizontalLayout)


        self.verticalLayout_2.addLayout(self.verticalLayout)


        self.horizontalLayout_2.addLayout(self.verticalLayout_2)


        self.retranslateUi(EditSectionWidget)

        QMetaObject.connectSlotsByName(EditSectionWidget)
    # setupUi

    def retranslateUi(self, EditSectionWidget):
        EditSectionWidget.setWindowTitle(QCoreApplication.translate("EditSectionWidget", u"Form", None))
        self.label.setText(QCoreApplication.translate("EditSectionWidget", u"Section: ", None))
        self.edit_button.setText(QCoreApplication.translate("EditSectionWidget", u"Edit", None))
        self.confirm_button.setText(QCoreApplication.translate("EditSectionWidget", u"Confirm", None))
    # retranslateUi

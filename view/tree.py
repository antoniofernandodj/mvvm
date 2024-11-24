# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'tree.ui'
##
## Created by: Qt User Interface Compiler version 6.8.0
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
from PySide6.QtWidgets import (QApplication, QFrame, QGridLayout, QHBoxLayout,
    QHeaderView, QLabel, QLineEdit, QListView,
    QMainWindow, QMenuBar, QPushButton, QSizePolicy,
    QStatusBar, QToolButton, QTreeView, QVBoxLayout,
    QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(800, 600)
        self.actionUpload = QAction(MainWindow)
        self.actionUpload.setObjectName(u"actionUpload")
        self.actionDownload = QAction(MainWindow)
        self.actionDownload.setObjectName(u"actionDownload")
        self.actionRename = QAction(MainWindow)
        self.actionRename.setObjectName(u"actionRename")
        self.actionShare = QAction(MainWindow)
        self.actionShare.setObjectName(u"actionShare")
        self.actionRemove = QAction(MainWindow)
        self.actionRemove.setObjectName(u"actionRemove")
        self.actionInfo = QAction(MainWindow)
        self.actionInfo.setObjectName(u"actionInfo")
        self.actionNew_folder = QAction(MainWindow)
        self.actionNew_folder.setObjectName(u"actionNew_folder")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.horizontalLayout_2 = QHBoxLayout(self.centralwidget)
        self.horizontalLayout_2.setSpacing(2)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(3, 3, 3, 3)
        self.frame_4 = QFrame(self.centralwidget)
        self.frame_4.setObjectName(u"frame_4")
        self.frame_4.setMaximumSize(QSize(300, 16777215))
        self.frame_4.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_4.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout = QVBoxLayout(self.frame_4)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.treeView = QTreeView(self.frame_4)
        self.treeView.setObjectName(u"treeView")
        self.treeView.setStyleSheet(u"border: 0px;")

        self.verticalLayout.addWidget(self.treeView)


        self.horizontalLayout_2.addWidget(self.frame_4)

        self.frame = QFrame(self.centralwidget)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_2 = QVBoxLayout(self.frame)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.frame_2 = QFrame(self.frame)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout = QGridLayout(self.frame_2)
        self.gridLayout.setObjectName(u"gridLayout")
        self.voltar_button = QToolButton(self.frame_2)
        self.voltar_button.setObjectName(u"voltar_button")

        self.gridLayout.addWidget(self.voltar_button, 0, 2, 1, 1)

        self.ir_button = QPushButton(self.frame_2)
        self.ir_button.setObjectName(u"ir_button")

        self.gridLayout.addWidget(self.ir_button, 0, 4, 1, 1)

        self.lineEdit = QLineEdit(self.frame_2)
        self.lineEdit.setObjectName(u"lineEdit")
        self.lineEdit.setStyleSheet(u"padding-left: 5px; padding-right: 5px;")

        self.gridLayout.addWidget(self.lineEdit, 0, 3, 1, 1)

        self.nova_pasta = QToolButton(self.frame_2)
        self.nova_pasta.setObjectName(u"nova_pasta")

        self.gridLayout.addWidget(self.nova_pasta, 0, 1, 1, 1)

        self.upload_button = QToolButton(self.frame_2)
        self.upload_button.setObjectName(u"upload_button")

        self.gridLayout.addWidget(self.upload_button, 0, 0, 1, 1)


        self.verticalLayout_2.addWidget(self.frame_2)

        self.listView = QListView(self.frame)
        self.listView.setObjectName(u"listView")
        self.listView.setStyleSheet(u"border: 0px;")

        self.verticalLayout_2.addWidget(self.listView)

        self.frame_3 = QFrame(self.frame)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setStyleSheet(u"QFrame{ border: 0px; }")
        self.frame_3.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_3.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout = QHBoxLayout(self.frame_3)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.aux_label = QLabel(self.frame_3)
        self.aux_label.setObjectName(u"aux_label")
        self.aux_label.setEnabled(True)
        self.aux_label.setMaximumSize(QSize(50, 16777215))
        self.aux_label.setStyleSheet(u"")
        self.aux_label.setLineWidth(1)

        self.horizontalLayout.addWidget(self.aux_label)

        self.cutted_label = QLabel(self.frame_3)
        self.cutted_label.setObjectName(u"cutted_label")

        self.horizontalLayout.addWidget(self.cutted_label)

        self.colar_aqui_button = QToolButton(self.frame_3)
        self.colar_aqui_button.setObjectName(u"colar_aqui_button")

        self.horizontalLayout.addWidget(self.colar_aqui_button)


        self.verticalLayout_2.addWidget(self.frame_3)


        self.horizontalLayout_2.addWidget(self.frame)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 800, 23))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.actionUpload.setText(QCoreApplication.translate("MainWindow", u"Upload", None))
        self.actionDownload.setText(QCoreApplication.translate("MainWindow", u"Download", None))
        self.actionRename.setText(QCoreApplication.translate("MainWindow", u"Rename", None))
        self.actionShare.setText(QCoreApplication.translate("MainWindow", u"Share", None))
        self.actionRemove.setText(QCoreApplication.translate("MainWindow", u"Remove", None))
        self.actionInfo.setText(QCoreApplication.translate("MainWindow", u"Info", None))
        self.actionNew_folder.setText(QCoreApplication.translate("MainWindow", u"New folder", None))
        self.voltar_button.setText(QCoreApplication.translate("MainWindow", u"Voltar", None))
        self.ir_button.setText(QCoreApplication.translate("MainWindow", u"Ir", None))
        self.nova_pasta.setText(QCoreApplication.translate("MainWindow", u"Nova Pasta", None))
        self.upload_button.setText(QCoreApplication.translate("MainWindow", u"Upload", None))
        self.aux_label.setText(QCoreApplication.translate("MainWindow", u"Cut:", None))
        self.cutted_label.setText("")
        self.colar_aqui_button.setText(QCoreApplication.translate("MainWindow", u"Colar aqui", None))
    # retranslateUi


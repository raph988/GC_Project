# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'interface_GC\accueil.ui'
#
# Created: Thu Mar 30 00:27:00 2017
#      by: pyside-uic 0.2.15 running on PySide 1.2.4
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_Accueil(object):
    def setupUi(self, Accueil):
        Accueil.setObjectName("Accueil")
        Accueil.resize(254, 300)
        Accueil.setMinimumSize(QtCore.QSize(254, 300))
        Accueil.setMaximumSize(QtCore.QSize(254, 300))
        self.centralwidget = QtGui.QWidget(Accueil)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.b_new_ctr = QtGui.QPushButton(self.centralwidget)
        self.b_new_ctr.setMinimumSize(QtCore.QSize(200, 50))
        self.b_new_ctr.setObjectName("b_new_ctr")
        self.verticalLayout.addWidget(self.b_new_ctr)
        self.b_edit_ctr = QtGui.QPushButton(self.centralwidget)
        self.b_edit_ctr.setMinimumSize(QtCore.QSize(200, 50))
        self.b_edit_ctr.setObjectName("b_edit_ctr")
        self.verticalLayout.addWidget(self.b_edit_ctr)
        self.b_livraison = QtGui.QPushButton(self.centralwidget)
        self.b_livraison.setMinimumSize(QtCore.QSize(200, 50))
        self.b_livraison.setObjectName("b_livraison")
        self.verticalLayout.addWidget(self.b_livraison)
        self.horizontalLayout.addLayout(self.verticalLayout)
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem2)
        spacerItem3 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem3)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        Accueil.setCentralWidget(self.centralwidget)
        self.statusbar = QtGui.QStatusBar(Accueil)
        self.statusbar.setObjectName("statusbar")
        Accueil.setStatusBar(self.statusbar)

        self.retranslateUi(Accueil)
        QtCore.QMetaObject.connectSlotsByName(Accueil)

    def retranslateUi(self, Accueil):
        Accueil.setWindowTitle(QtGui.QApplication.translate("Accueil", "MainWindow", None, QtGui.QApplication.UnicodeUTF8))
        self.b_new_ctr.setText(QtGui.QApplication.translate("Accueil", "Nouveau contrat", None, QtGui.QApplication.UnicodeUTF8))
        self.b_edit_ctr.setText(QtGui.QApplication.translate("Accueil", "Modifier un contrat", None, QtGui.QApplication.UnicodeUTF8))
        self.b_livraison.setText(QtGui.QApplication.translate("Accueil", "Nouvelle livraison", None, QtGui.QApplication.UnicodeUTF8))


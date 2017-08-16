# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'interface_GC\accueil.ui'
#
# Created: Tue Jun 06 01:03:19 2017
#      by: pyside-uic 0.2.15 running on PySide 1.2.4
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_Accueil(object):
    def setupUi(self, Accueil):
        Accueil.setObjectName("Accueil")
        Accueil.resize(677, 559)
        self.w_centralwidget = QtGui.QWidget(Accueil)
        self.w_centralwidget.setStyleSheet("")
        self.w_centralwidget.setObjectName("w_centralwidget")
        self.verticalLayout = QtGui.QVBoxLayout(self.w_centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.splitter = QtGui.QSplitter(self.w_centralwidget)
        self.splitter.setStyleSheet("")
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")
        self.f_contracts = QtGui.QFrame(self.splitter)
        self.f_contracts.setObjectName("f_contracts")
        self.f_deliveries = QtGui.QFrame(self.splitter)
        self.f_deliveries.setObjectName("f_deliveries")
        self.verticalLayout.addWidget(self.splitter)
        Accueil.setCentralWidget(self.w_centralwidget)
        self.menuBar = QtGui.QMenuBar(Accueil)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 677, 26))
        self.menuBar.setObjectName("menuBar")
        self.menuMise_jour = QtGui.QMenu(self.menuBar)
        self.menuMise_jour.setObjectName("menuMise_jour")
        self.menuA_propos = QtGui.QMenu(self.menuBar)
        self.menuA_propos.setObjectName("menuA_propos")
        Accueil.setMenuBar(self.menuBar)
        self.actionFIF = QtGui.QAction(Accueil)
        self.actionFIF.setObjectName("actionFIF")
        self.actionFIA = QtGui.QAction(Accueil)
        self.actionFIA.setObjectName("actionFIA")
        self.actionConfig = QtGui.QAction(Accueil)
        self.actionConfig.setObjectName("actionConfig")
        self.menuMise_jour.addAction(self.actionFIF)
        self.menuMise_jour.addAction(self.actionFIA)
        self.menuMise_jour.addAction(self.actionConfig)
        self.menuBar.addAction(self.menuMise_jour.menuAction())
        self.menuBar.addAction(self.menuA_propos.menuAction())

        self.retranslateUi(Accueil)
        QtCore.QMetaObject.connectSlotsByName(Accueil)

    def retranslateUi(self, Accueil):
        Accueil.setWindowTitle(QtGui.QApplication.translate("Accueil", "Accueil", None, QtGui.QApplication.UnicodeUTF8))
        self.menuMise_jour.setTitle(QtGui.QApplication.translate("Accueil", "Mettre à jour", None, QtGui.QApplication.UnicodeUTF8))
        self.menuA_propos.setTitle(QtGui.QApplication.translate("Accueil", "A propos", None, QtGui.QApplication.UnicodeUTF8))
        self.actionFIF.setText(QtGui.QApplication.translate("Accueil", "La base fournisseurs (fif.xslx)", None, QtGui.QApplication.UnicodeUTF8))
        self.actionFIA.setText(QtGui.QApplication.translate("Accueil", "La base clients (fia.xlsx)", None, QtGui.QApplication.UnicodeUTF8))
        self.actionConfig.setText(QtGui.QApplication.translate("Accueil", "Les données de configuration (Config.xlsx)", None, QtGui.QApplication.UnicodeUTF8))


# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'interface_GC\ui_contract_initer.ui'
#
# Created: Tue May 30 00:45:42 2017
#      by: pyside-uic 0.2.15 running on PySide 1.2.4
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(980, 970)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout_3 = QtGui.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.tab_main = QtGui.QTabWidget(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(9)
        self.tab_main.setFont(font)
        self.tab_main.setObjectName("tab_main")
        self.tab_simulation = QtGui.QWidget()
        self.tab_simulation.setObjectName("tab_simulation")
        self.horizontalLayout_3 = QtGui.QHBoxLayout(self.tab_simulation)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.verticalLayout_4 = QtGui.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.horizontalLayout_6 = QtGui.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_17 = QtGui.QLabel(self.tab_simulation)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(9)
        self.label_17.setFont(font)
        self.label_17.setObjectName("label_17")
        self.horizontalLayout_2.addWidget(self.label_17)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.gb_type = QtGui.QGroupBox(self.tab_simulation)
        self.gb_type.setTitle("")
        self.gb_type.setObjectName("gb_type")
        self.horizontalLayout_4 = QtGui.QHBoxLayout(self.gb_type)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.rb_fournisseur = QtGui.QRadioButton(self.gb_type)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(9)
        self.rb_fournisseur.setFont(font)
        self.rb_fournisseur.setObjectName("rb_fournisseur")
        self.horizontalLayout_4.addWidget(self.rb_fournisseur)
        self.line_2 = QtGui.QFrame(self.gb_type)
        self.line_2.setFrameShape(QtGui.QFrame.VLine)
        self.line_2.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.horizontalLayout_4.addWidget(self.line_2)
        self.rb_acheteur = QtGui.QRadioButton(self.gb_type)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(9)
        self.rb_acheteur.setFont(font)
        self.rb_acheteur.setObjectName("rb_acheteur")
        self.horizontalLayout_4.addWidget(self.rb_acheteur)
        self.horizontalLayout_2.addWidget(self.gb_type)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.horizontalLayout_6.addLayout(self.horizontalLayout_2)
        self.verticalLayout_4.addLayout(self.horizontalLayout_6)
        self.horizontalLayout_5 = QtGui.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.label_18 = QtGui.QLabel(self.tab_simulation)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(9)
        self.label_18.setFont(font)
        self.label_18.setObjectName("label_18")
        self.horizontalLayout_5.addWidget(self.label_18)
        self.produit = QtGui.QLineEdit(self.tab_simulation)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(9)
        self.produit.setFont(font)
        self.produit.setObjectName("produit")
        self.horizontalLayout_5.addWidget(self.produit)
        self.cb_enlarge = QtGui.QCheckBox(self.tab_simulation)
        self.cb_enlarge.setObjectName("cb_enlarge")
        self.horizontalLayout_5.addWidget(self.cb_enlarge)
        self.verticalLayout_4.addLayout(self.horizontalLayout_5)
        self.line = QtGui.QFrame(self.tab_simulation)
        self.line.setMinimumSize(QtCore.QSize(0, 20))
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout_4.addWidget(self.line)
        self.gb_result = QtGui.QGroupBox(self.tab_simulation)
        self.gb_result.setObjectName("gb_result")
        self.verticalLayout_14 = QtGui.QVBoxLayout(self.gb_result)
        self.verticalLayout_14.setObjectName("verticalLayout_14")
        self.horizontalLayout_9 = QtGui.QHBoxLayout()
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_9.addItem(spacerItem2)
        self.label_22 = QtGui.QLabel(self.gb_result)
        self.label_22.setObjectName("label_22")
        self.horizontalLayout_9.addWidget(self.label_22)
        self.cb_classifier = QtGui.QComboBox(self.gb_result)
        self.cb_classifier.setEnabled(False)
        self.cb_classifier.setObjectName("cb_classifier")
        self.cb_classifier.addItem("")
        self.cb_classifier.addItem("")
        self.cb_classifier.addItem("")
        self.horizontalLayout_9.addWidget(self.cb_classifier)
        self.cb_conteneur = QtGui.QComboBox(self.gb_result)
        self.cb_conteneur.setEnabled(False)
        self.cb_conteneur.setObjectName("cb_conteneur")
        self.horizontalLayout_9.addWidget(self.cb_conteneur)
        self.verticalLayout_14.addLayout(self.horizontalLayout_9)
        self.scroll_result = QtGui.QScrollArea(self.gb_result)
        self.scroll_result.setAutoFillBackground(True)
        self.scroll_result.setFrameShadow(QtGui.QFrame.Plain)
        self.scroll_result.setLineWidth(0)
        self.scroll_result.setWidgetResizable(True)
        self.scroll_result.setObjectName("scroll_result")
        self.scrollAreaWidgetContents = QtGui.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 898, 597))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.verticalLayout_12 = QtGui.QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_12.setObjectName("verticalLayout_12")
        self.result_layout = QtGui.QVBoxLayout()
        self.result_layout.setObjectName("result_layout")
        self.verticalLayout_12.addLayout(self.result_layout)
        self.scroll_result.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout_14.addWidget(self.scroll_result)
        self.verticalLayout_4.addWidget(self.gb_result)
        self.horizontalLayout_8 = QtGui.QHBoxLayout()
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        spacerItem3 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_8.addItem(spacerItem3)
        self.b_reset_simul = QtGui.QPushButton(self.tab_simulation)
        self.b_reset_simul.setObjectName("b_reset_simul")
        self.horizontalLayout_8.addWidget(self.b_reset_simul)
        self.verticalLayout_11 = QtGui.QVBoxLayout()
        self.verticalLayout_11.setObjectName("verticalLayout_11")
        self.b_rechercher = QtGui.QPushButton(self.tab_simulation)
        self.b_rechercher.setMinimumSize(QtCore.QSize(56, 40))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(9)
        font.setWeight(75)
        font.setBold(True)
        self.b_rechercher.setFont(font)
        self.b_rechercher.setObjectName("b_rechercher")
        self.verticalLayout_11.addWidget(self.b_rechercher)
        self.b_next = QtGui.QPushButton(self.tab_simulation)
        self.b_next.setMinimumSize(QtCore.QSize(56, 40))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(9)
        font.setWeight(75)
        font.setBold(True)
        self.b_next.setFont(font)
        self.b_next.setObjectName("b_next")
        self.verticalLayout_11.addWidget(self.b_next)
        self.horizontalLayout_8.addLayout(self.verticalLayout_11)
        self.verticalLayout_4.addLayout(self.horizontalLayout_8)
        self.horizontalLayout_3.addLayout(self.verticalLayout_4)
        self.tab_main.addTab(self.tab_simulation, "")
        self.verticalLayout_3.addWidget(self.tab_main)
        self.verticalLayout.addLayout(self.verticalLayout_3)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        self.tab_main.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "MainWindow", None, QtGui.QApplication.UnicodeUTF8))
        self.label_17.setText(QtGui.QApplication.translate("MainWindow", "Rechercher un :", None, QtGui.QApplication.UnicodeUTF8))
        self.rb_fournisseur.setText(QtGui.QApplication.translate("MainWindow", "Fournisseur", None, QtGui.QApplication.UnicodeUTF8))
        self.rb_acheteur.setText(QtGui.QApplication.translate("MainWindow", "Acheteur", None, QtGui.QApplication.UnicodeUTF8))
        self.label_18.setText(QtGui.QApplication.translate("MainWindow", "Marchandise :", None, QtGui.QApplication.UnicodeUTF8))
        self.cb_enlarge.setText(QtGui.QApplication.translate("MainWindow", "Élargir la recherche", None, QtGui.QApplication.UnicodeUTF8))
        self.gb_result.setTitle(QtGui.QApplication.translate("MainWindow", "Resultat(s) :", None, QtGui.QApplication.UnicodeUTF8))
        self.label_22.setText(QtGui.QApplication.translate("MainWindow", "Ordonner par", None, QtGui.QApplication.UnicodeUTF8))
        self.cb_classifier.setItemText(0, QtGui.QApplication.translate("MainWindow", "Pertinence", None, QtGui.QApplication.UnicodeUTF8))
        self.cb_classifier.setItemText(1, QtGui.QApplication.translate("MainWindow", "Pays", None, QtGui.QApplication.UnicodeUTF8))
        self.cb_classifier.setItemText(2, QtGui.QApplication.translate("MainWindow", "Conteneur", None, QtGui.QApplication.UnicodeUTF8))
        self.b_reset_simul.setText(QtGui.QApplication.translate("MainWindow", "Reset", None, QtGui.QApplication.UnicodeUTF8))
        self.b_rechercher.setText(QtGui.QApplication.translate("MainWindow", "Rechercher", None, QtGui.QApplication.UnicodeUTF8))
        self.b_next.setText(QtGui.QApplication.translate("MainWindow", "Passer au contrat !", None, QtGui.QApplication.UnicodeUTF8))
        self.tab_main.setTabText(self.tab_main.indexOf(self.tab_simulation), QtGui.QApplication.translate("MainWindow", "Recherche", None, QtGui.QApplication.UnicodeUTF8))


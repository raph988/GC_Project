# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'interface_GC\ui_delivery_manager.ui'
#
# Created: Fri May 19 15:11:27 2017
#      by: pyside-uic 0.2.15 running on PySide 1.2.4
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        MainWindow.setStyleSheet("")
        self.dlv_centralwidget = QtGui.QWidget(MainWindow)
        self.dlv_centralwidget.setObjectName("dlv_centralwidget")
        self.verticalLayout = QtGui.QVBoxLayout(self.dlv_centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_4 = QtGui.QLabel(self.dlv_centralwidget)
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setItalic(True)
        self.label_4.setFont(font)
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_2.addWidget(self.label_4)
        self.verticalLayout.addLayout(self.verticalLayout_2)
        self.horizontalLayout_5 = QtGui.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.groupBox_2 = QtGui.QGroupBox(self.dlv_centralwidget)
        self.groupBox_2.setStyleSheet("")
        self.groupBox_2.setObjectName("groupBox_2")
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.groupBox_2)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.gridLayout_2 = QtGui.QGridLayout()
        self.gridLayout_2.setSizeConstraint(QtGui.QLayout.SetNoConstraint)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.horizontalLayout_6 = QtGui.QHBoxLayout()
        self.horizontalLayout_6.setSizeConstraint(QtGui.QLayout.SetMinimumSize)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.verticalLayout_5 = QtGui.QVBoxLayout()
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.cb_year = QtGui.QComboBox(self.groupBox_2)
        self.cb_year.setObjectName("cb_year")
        self.verticalLayout_5.addWidget(self.cb_year)
        self.cb_month = QtGui.QComboBox(self.groupBox_2)
        self.cb_month.setObjectName("cb_month")
        self.verticalLayout_5.addWidget(self.cb_month)
        self.verticalLayout_6 = QtGui.QVBoxLayout()
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.rb_date_appel = QtGui.QRadioButton(self.groupBox_2)
        self.rb_date_appel.setObjectName("rb_date_appel")
        self.verticalLayout_6.addWidget(self.rb_date_appel)
        self.rb_date_livr = QtGui.QRadioButton(self.groupBox_2)
        self.rb_date_livr.setObjectName("rb_date_livr")
        self.verticalLayout_6.addWidget(self.rb_date_livr)
        self.verticalLayout_5.addLayout(self.verticalLayout_6)
        self.horizontalLayout_6.addLayout(self.verticalLayout_5)
        self.gridLayout_2.addLayout(self.horizontalLayout_6, 1, 0, 1, 1)
        self.verticalLayout_4 = QtGui.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_5 = QtGui.QLabel(self.groupBox_2)
        self.label_5.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_5.setObjectName("label_5")
        self.horizontalLayout_3.addWidget(self.label_5)
        self.cb_sort_client = QtGui.QComboBox(self.groupBox_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cb_sort_client.sizePolicy().hasHeightForWidth())
        self.cb_sort_client.setSizePolicy(sizePolicy)
        self.cb_sort_client.setSizeAdjustPolicy(QtGui.QComboBox.AdjustToContents)
        self.cb_sort_client.setObjectName("cb_sort_client")
        self.horizontalLayout_3.addWidget(self.cb_sort_client)
        self.verticalLayout_4.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_9 = QtGui.QLabel(self.groupBox_2)
        self.label_9.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_9.setObjectName("label_9")
        self.horizontalLayout_2.addWidget(self.label_9)
        self.cb_sort_fourniss_2 = QtGui.QComboBox(self.groupBox_2)
        self.cb_sort_fourniss_2.setObjectName("cb_sort_fourniss_2")
        self.horizontalLayout_2.addWidget(self.cb_sort_fourniss_2)
        self.verticalLayout_4.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_7 = QtGui.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.label_10 = QtGui.QLabel(self.groupBox_2)
        self.label_10.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_10.setObjectName("label_10")
        self.horizontalLayout_7.addWidget(self.label_10)
        self.cb_marchandise = QtGui.QComboBox(self.groupBox_2)
        self.cb_marchandise.setObjectName("cb_marchandise")
        self.horizontalLayout_7.addWidget(self.cb_marchandise)
        self.verticalLayout_4.addLayout(self.horizontalLayout_7)
        self.gridLayout_2.addLayout(self.verticalLayout_4, 1, 2, 1, 1)
        self.label_3 = QtGui.QLabel(self.groupBox_2)
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.gridLayout_2.addWidget(self.label_3, 0, 0, 1, 1)
        self.label_7 = QtGui.QLabel(self.groupBox_2)
        self.label_7.setAlignment(QtCore.Qt.AlignCenter)
        self.label_7.setObjectName("label_7")
        self.gridLayout_2.addWidget(self.label_7, 0, 2, 1, 1)
        self.line = QtGui.QFrame(self.groupBox_2)
        self.line.setFrameShape(QtGui.QFrame.VLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName("line")
        self.gridLayout_2.addWidget(self.line, 1, 1, 1, 1)
        self.verticalLayout_3.addLayout(self.gridLayout_2)
        self.horizontalLayout_5.addWidget(self.groupBox_2)
        self.groupBox = QtGui.QGroupBox(self.dlv_centralwidget)
        self.groupBox.setObjectName("groupBox")
        self.horizontalLayout_4 = QtGui.QHBoxLayout(self.groupBox)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.label_8 = QtGui.QLabel(self.groupBox)
        self.label_8.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_8.setObjectName("label_8")
        self.gridLayout.addWidget(self.label_8, 1, 1, 1, 1)
        self.rb_ref_fourniss = QtGui.QRadioButton(self.groupBox)
        self.rb_ref_fourniss.setText("")
        self.rb_ref_fourniss.setObjectName("rb_ref_fourniss")
        self.gridLayout.addWidget(self.rb_ref_fourniss, 1, 0, 1, 1)
        self.rb_ref_client = QtGui.QRadioButton(self.groupBox)
        self.rb_ref_client.setText("")
        self.rb_ref_client.setObjectName("rb_ref_client")
        self.gridLayout.addWidget(self.rb_ref_client, 0, 0, 1, 1)
        self.l_ref_fourniss = QtGui.QLineEdit(self.groupBox)
        self.l_ref_fourniss.setObjectName("l_ref_fourniss")
        self.gridLayout.addWidget(self.l_ref_fourniss, 1, 2, 1, 1)
        self.rb_ref_charg = QtGui.QRadioButton(self.groupBox)
        self.rb_ref_charg.setText("")
        self.rb_ref_charg.setObjectName("rb_ref_charg")
        self.gridLayout.addWidget(self.rb_ref_charg, 2, 0, 1, 1)
        self.l_ref_charg = QtGui.QLineEdit(self.groupBox)
        self.l_ref_charg.setObjectName("l_ref_charg")
        self.gridLayout.addWidget(self.l_ref_charg, 2, 2, 1, 1)
        self.b_rechercher = QtGui.QPushButton(self.groupBox)
        self.b_rechercher.setObjectName("b_rechercher")
        self.gridLayout.addWidget(self.b_rechercher, 3, 2, 1, 1)
        self.l_ref_client = QtGui.QLineEdit(self.groupBox)
        self.l_ref_client.setObjectName("l_ref_client")
        self.gridLayout.addWidget(self.l_ref_client, 0, 2, 1, 1)
        self.label = QtGui.QLabel(self.groupBox)
        self.label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 1, 1, 1)
        self.label_2 = QtGui.QLabel(self.groupBox)
        self.label_2.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 2, 1, 1, 1)
        self.b_reinit_list = QtGui.QPushButton(self.groupBox)
        self.b_reinit_list.setObjectName("b_reinit_list")
        self.gridLayout.addWidget(self.b_reinit_list, 3, 1, 1, 1)
        self.horizontalLayout_4.addLayout(self.gridLayout)
        self.horizontalLayout_5.addWidget(self.groupBox)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem)
        self.verticalLayout.addLayout(self.horizontalLayout_5)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.t_deliver_list = QtGui.QTreeWidget(self.dlv_centralwidget)
        self.t_deliver_list.setStyleSheet("")
        self.t_deliver_list.setEditTriggers(QtGui.QAbstractItemView.DoubleClicked|QtGui.QAbstractItemView.EditKeyPressed)
        self.t_deliver_list.setProperty("showDropIndicator", False)
        self.t_deliver_list.setItemsExpandable(True)
        self.t_deliver_list.setObjectName("t_deliver_list")
        self.t_deliver_list.headerItem().setText(0, "1")
        self.t_deliver_list.header().setSortIndicatorShown(True)
        self.horizontalLayout.addWidget(self.t_deliver_list)
        self.verticalLayout.addLayout(self.horizontalLayout)
        MainWindow.setCentralWidget(self.dlv_centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "MainWindow", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("MainWindow", "Gestionnaire de livraisons", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_2.setTitle(QtGui.QApplication.translate("MainWindow", "Afficher les livraisons selon :", None, QtGui.QApplication.UnicodeUTF8))
        self.rb_date_appel.setText(QtGui.QApplication.translate("MainWindow", "Date d\'appel", None, QtGui.QApplication.UnicodeUTF8))
        self.rb_date_livr.setText(QtGui.QApplication.translate("MainWindow", "Date de charg./livr.", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setText(QtGui.QApplication.translate("MainWindow", "Client :", None, QtGui.QApplication.UnicodeUTF8))
        self.label_9.setText(QtGui.QApplication.translate("MainWindow", "Fournisseur :", None, QtGui.QApplication.UnicodeUTF8))
        self.label_10.setText(QtGui.QApplication.translate("MainWindow", "Marchandise :", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("MainWindow", "Date", None, QtGui.QApplication.UnicodeUTF8))
        self.label_7.setText(QtGui.QApplication.translate("MainWindow", "Nom", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("MainWindow", "Recherche une livraison par :", None, QtGui.QApplication.UnicodeUTF8))
        self.label_8.setText(QtGui.QApplication.translate("MainWindow", "référence fournisseur :", None, QtGui.QApplication.UnicodeUTF8))
        self.b_rechercher.setText(QtGui.QApplication.translate("MainWindow", "Rechercher", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("MainWindow", "référence client :", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("MainWindow", "référence chargement :", None, QtGui.QApplication.UnicodeUTF8))
        self.b_reinit_list.setText(QtGui.QApplication.translate("MainWindow", "Réinitialiser la liste", None, QtGui.QApplication.UnicodeUTF8))

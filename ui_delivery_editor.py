# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'interface_GC\ui_delivery_editor.ui'
#
# Created: Tue May 30 12:05:44 2017
#      by: pyside-uic 0.2.15 running on PySide 1.2.4
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_ui_delivery_editor(object):
    def setupUi(self, ui_delivery_editor):
        ui_delivery_editor.setObjectName("ui_delivery_editor")
        ui_delivery_editor.resize(609, 313)
        self.verticalLayout = QtGui.QVBoxLayout(ui_delivery_editor)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.formLayout = QtGui.QFormLayout()
        self.formLayout.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout.setObjectName("formLayout")
        self.label = QtGui.QLabel(ui_delivery_editor)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setMinimumSize(QtCore.QSize(180, 0))
        self.label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.label)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.rb_depart = QtGui.QRadioButton(ui_delivery_editor)
        self.rb_depart.setObjectName("rb_depart")
        self.horizontalLayout_3.addWidget(self.rb_depart)
        self.rb_franco = QtGui.QRadioButton(ui_delivery_editor)
        self.rb_franco.setObjectName("rb_franco")
        self.horizontalLayout_3.addWidget(self.rb_franco)
        self.formLayout.setLayout(0, QtGui.QFormLayout.FieldRole, self.horizontalLayout_3)
        self.label_2 = QtGui.QLabel(ui_delivery_editor)
        self.label_2.setMinimumSize(QtCore.QSize(180, 0))
        self.label_2.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.label_2)
        self.label_3 = QtGui.QLabel(ui_delivery_editor)
        self.label_3.setMinimumSize(QtCore.QSize(180, 0))
        self.label_3.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.label_3)
        self.horizontalLayout_5 = QtGui.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.cb_date = QtGui.QComboBox(ui_delivery_editor)
        self.cb_date.setObjectName("cb_date")
        self.horizontalLayout_5.addWidget(self.cb_date)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem)
        self.formLayout.setLayout(2, QtGui.QFormLayout.FieldRole, self.horizontalLayout_5)
        self.label_14 = QtGui.QLabel(ui_delivery_editor)
        self.label_14.setMinimumSize(QtCore.QSize(180, 0))
        self.label_14.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_14.setObjectName("label_14")
        self.formLayout.setWidget(4, QtGui.QFormLayout.LabelRole, self.label_14)
        self.l_horaire = QtGui.QLineEdit(ui_delivery_editor)
        self.l_horaire.setObjectName("l_horaire")
        self.formLayout.setWidget(4, QtGui.QFormLayout.FieldRole, self.l_horaire)
        self.label_5 = QtGui.QLabel(ui_delivery_editor)
        self.label_5.setMinimumSize(QtCore.QSize(180, 0))
        self.label_5.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_5.setObjectName("label_5")
        self.formLayout.setWidget(5, QtGui.QFormLayout.LabelRole, self.label_5)
        self.l_qte = QtGui.QLineEdit(ui_delivery_editor)
        self.l_qte.setObjectName("l_qte")
        self.formLayout.setWidget(5, QtGui.QFormLayout.FieldRole, self.l_qte)
        self.label_6 = QtGui.QLabel(ui_delivery_editor)
        self.label_6.setMinimumSize(QtCore.QSize(180, 0))
        self.label_6.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_6.setObjectName("label_6")
        self.formLayout.setWidget(6, QtGui.QFormLayout.LabelRole, self.label_6)
        self.l_marchandise = QtGui.QLineEdit(ui_delivery_editor)
        self.l_marchandise.setObjectName("l_marchandise")
        self.formLayout.setWidget(6, QtGui.QFormLayout.FieldRole, self.l_marchandise)
        self.label_7 = QtGui.QLabel(ui_delivery_editor)
        self.label_7.setMinimumSize(QtCore.QSize(180, 0))
        self.label_7.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_7.setObjectName("label_7")
        self.formLayout.setWidget(7, QtGui.QFormLayout.LabelRole, self.label_7)
        self.l_ref_fourniss = QtGui.QLineEdit(ui_delivery_editor)
        self.l_ref_fourniss.setObjectName("l_ref_fourniss")
        self.formLayout.setWidget(7, QtGui.QFormLayout.FieldRole, self.l_ref_fourniss)
        self.label_9 = QtGui.QLabel(ui_delivery_editor)
        self.label_9.setMinimumSize(QtCore.QSize(180, 0))
        self.label_9.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_9.setObjectName("label_9")
        self.formLayout.setWidget(8, QtGui.QFormLayout.LabelRole, self.label_9)
        self.l_ref_client = QtGui.QLineEdit(ui_delivery_editor)
        self.l_ref_client.setObjectName("l_ref_client")
        self.formLayout.setWidget(8, QtGui.QFormLayout.FieldRole, self.l_ref_client)
        self.label_10 = QtGui.QLabel(ui_delivery_editor)
        self.label_10.setMinimumSize(QtCore.QSize(180, 0))
        self.label_10.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_10.setObjectName("label_10")
        self.formLayout.setWidget(9, QtGui.QFormLayout.LabelRole, self.label_10)
        self.l_ref_charg = QtGui.QLineEdit(ui_delivery_editor)
        self.l_ref_charg.setObjectName("l_ref_charg")
        self.formLayout.setWidget(9, QtGui.QFormLayout.FieldRole, self.l_ref_charg)
        self.label_44 = QtGui.QLabel(ui_delivery_editor)
        self.label_44.setMinimumSize(QtCore.QSize(180, 0))
        self.label_44.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_44.setObjectName("label_44")
        self.formLayout.setWidget(3, QtGui.QFormLayout.LabelRole, self.label_44)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.d_date_reelle = QtGui.QDateEdit(ui_delivery_editor)
        self.d_date_reelle.setObjectName("d_date_reelle")
        self.horizontalLayout_2.addWidget(self.d_date_reelle)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.formLayout.setLayout(3, QtGui.QFormLayout.FieldRole, self.horizontalLayout_2)
        self.cb_ville = QtGui.QComboBox(ui_delivery_editor)
        self.cb_ville.setObjectName("cb_ville")
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.cb_ville)
        self.horizontalLayout.addLayout(self.formLayout)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(ui_delivery_editor)
        QtCore.QMetaObject.connectSlotsByName(ui_delivery_editor)

    def retranslateUi(self, ui_delivery_editor):
        ui_delivery_editor.setWindowTitle(QtGui.QApplication.translate("ui_delivery_editor", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("ui_delivery_editor", "Type de livraison :", None, QtGui.QApplication.UnicodeUTF8))
        self.rb_depart.setText(QtGui.QApplication.translate("ui_delivery_editor", "Départ", None, QtGui.QApplication.UnicodeUTF8))
        self.rb_franco.setText(QtGui.QApplication.translate("ui_delivery_editor", "Franco", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("ui_delivery_editor", "Adresse / Ville :", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("ui_delivery_editor", "Date initialement prévue :", None, QtGui.QApplication.UnicodeUTF8))
        self.label_14.setText(QtGui.QApplication.translate("ui_delivery_editor", "Horaire :", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setText(QtGui.QApplication.translate("ui_delivery_editor", "Quantité (en T):", None, QtGui.QApplication.UnicodeUTF8))
        self.label_6.setText(QtGui.QApplication.translate("ui_delivery_editor", "Marchandise :", None, QtGui.QApplication.UnicodeUTF8))
        self.label_7.setText(QtGui.QApplication.translate("ui_delivery_editor", "N° contrat fournisseur :", None, QtGui.QApplication.UnicodeUTF8))
        self.label_9.setText(QtGui.QApplication.translate("ui_delivery_editor", "Référence client :", None, QtGui.QApplication.UnicodeUTF8))
        self.label_10.setText(QtGui.QApplication.translate("ui_delivery_editor", "Référence chargement :", None, QtGui.QApplication.UnicodeUTF8))
        self.label_44.setText(QtGui.QApplication.translate("ui_delivery_editor", "Date effective :", None, QtGui.QApplication.UnicodeUTF8))


# -*- coding: utf-8 -*-
"""
Created on Tue Aug 15 17:58:11 2017

@author: Raph
"""

from PySide import QtGui, QtCore
import datetime

from classes import Market
from utils import number_of_days, format_num

from ui_delivery_editor import Ui_ui_delivery_editor as Ui_delivery_editor


        
class ui_new_delivery(QtGui.QWidget, QtCore.QObject):
    def __init__(self, parent = None):
        super(ui_new_delivery, self).__init__(parent)
        self.ui = Ui_delivery_editor()
        self.ui.setupUi(self)
        
class deliveryEditor(QtGui.QDialog, QtCore.QObject):
    def __init__(self, parent = None, ctr = None, delivery = None):
        super(deliveryEditor, self).__init__(parent)
        self.setWindowIcon(QtGui.QIcon('icone.png'))
        self.setWindowTitle('Éditeur de livraison')
        self.oil_market = Market()
        
        if ctr is None: return
        self.ctr = ctr
        self.mainWidget = ui_new_delivery(self)
        self.buttons = QtGui.QDialogButtonBox( QtGui.QDialogButtonBox.Cancel | QtGui.QDialogButtonBox.Ok, QtCore.Qt.Horizontal, self)
        self.buttons.button(QtGui.QDialogButtonBox.Ok).setText("Valider")
        self.buttons.button(QtGui.QDialogButtonBox.Cancel).setText("Annuler")
        self.doNotClose = False
        
        layout = QtGui.QVBoxLayout()
        layout.addWidget(self.mainWidget)
        mainLayout = QtGui.QVBoxLayout()
        mainLayout.addLayout(layout)
        mainLayout.addWidget(self.buttons)
        self.setLayout(mainLayout)

        self.mainWidget.ui.l_qte.setValidator(QtGui.QDoubleValidator(0.0, 999999.0, 10, self))
        self.buttons.accepted.connect(self.checkDelivery)
        self.buttons.rejected.connect(self.reject)
        self.mainWidget.ui.cb_ville.setEditable(True)
        self.mainWidget.ui.cb_date.currentIndexChanged.connect(self.dateSelected)
        self.mainWidget.ui.rb_franco.toggled.connect(self.delivTypeChanged)
        self.mainWidget.ui.rb_depart.toggled.connect(self.delivTypeChanged)
        
        
        self.initWidget()
        if delivery is not None:
            self.updateWidget(delivery)
                
    def initWidget(self):
        self.mainWidget.ui.l_marchandise.setText(self.oil_market.getMarchandiseFullName(self.ctr.marchandise))
        if self.ctr.is_franco is True:
            self.mainWidget.ui.rb_franco.setChecked(True)
        else:
            self.mainWidget.ui.rb_depart.setChecked(True)
        
        dlv_dic = self.ctr.periode_livraison
        ordered_years = sorted(dlv_dic.keys())
        for i in range(0, len(ordered_years), 1):
            y = ordered_years[i]
            for j in range(0, 12):
                m = str(j+1).zfill(2)
                total = format_num(dlv_dic[y][m]["total"])
                if float(total) == 0: continue
                date = m + '/' + str(y)
                self.mainWidget.ui.cb_date.addItem(date)
                
        if self.mainWidget.ui.cb_date.count() > 0:
            self.mainWidget.ui.cb_date.setCurrentIndex(0)

    def updateWidget(self, delivery):
#        delivery = Livraison()
        if delivery.date_charg_livr is not None:
            date = delivery.date_charg_livr.split('/')
            if len(date) > 2:
                m = date[1]
                y = date[2]
            elif len(date) == 0:
                m = "00"
                y = "0000"
            else:
                m = date[0]
                y = date[1]
            date = m+"/"+ y
            self.mainWidget.ui.cb_date.setCurrentIndex(self.mainWidget.ui.cb_date.findText(date))
#            self.mainWidget.ui.cb_jour.clear()
#            self.mainWidget.ui.cb_jour.addItems(list(str(j).zfill(2) for j in range(1, number_of_days(m,y)+1, 1)))

                
        if delivery.horaire_charg_livr is not None:
            self.mainWidget.ui.l_horaire.setText(delivery.horaire_charg_livr)
        if delivery.marchandise is not None:
            self.mainWidget.ui.l_marchandise.setText(delivery.marchandise)
        if delivery.quantite is not None:
            self.mainWidget.ui.l_qte.setText(delivery.quantite)
        if delivery.ref_client is not None:
            self.mainWidget.ui.l_ref_client.setText(delivery.ref_client)
        if delivery.ref_fourniss is not None:
            self.mainWidget.ui.l_ref_fourniss.setText(delivery.ref_fourniss)
        if delivery.ref_chargement is not None:
            self.mainWidget.ui.l_ref_charg.setText(delivery.ref_chargement)
            
                
    def dateSelected(self, index):
        sender = self.sender()
        if index < 0:
            return
        m, y = sender.itemText(index).split('/')[-2], sender.itemText(index).split('/')[-1]
        self.mainWidget.ui.d_date_reelle.setDate(QtCore.QDate.fromString('01/'+m+'/'+y, "dd/MM/yyyy"))
        total = format_num(self.ctr.periode_livraison[y][m]["total"])
        done = format_num(self.ctr.periode_livraison[y][m]["done"])
        maximum = format_num(float(total) - float(done) )
        self.mainWidget.ui.l_qte.setPlaceholderText('max: '+maximum)
        
        
    def delivTypeChanged(self):
        self.mainWidget.ui.cb_ville.clear()
        if self.mainWidget.ui.rb_franco.isChecked():
            adresses = self.ctr.getAcheteur().getUsineAdr()
            for adr, v, u in adresses:
                self.mainWidget.ui.cb_ville.addItem(adr, userData=v)
        else:
            adresses = self.ctr.getVendeur().getUsineAdr()
            for adr, v, u in adresses:
                self.mainWidget.ui.cb_ville.addItem(adr, userData=v)
            
            
    def checkDelivery(self):
        print "checkDelivery"
        to_complete = 0
        if self.mainWidget.ui.cb_date.currentIndex() < 0:
            to_complete += 1
            self.mainWidget.ui.cb_date.setStyleSheet("#cb_date { border: 3px solid red; }")
        else:
            self.mainWidget.ui.cb_date.setStyleSheet("")
            
        if self.mainWidget.ui.cb_ville.currentIndex() < 0:
            to_complete += 1
            self.mainWidget.ui.cb_ville.setStyleSheet("#cb_ville { border: 3px solid red; }")
        else:
            self.mainWidget.ui.cb_ville.setStyleSheet("")
            
        print self.mainWidget.ui.l_qte.text()
        if len(self.mainWidget.ui.l_qte.text()) < 1:
            to_complete += 1
            self.mainWidget.ui.l_qte.setStyleSheet("#l_qte { border: 3px solid red; }")
        else:
            self.mainWidget.ui.l_qte.setStyleSheet("")
            
        if len(self.mainWidget.ui.l_marchandise.text()) < 1:
            to_complete += 1
            self.mainWidget.ui.l_marchandise.setStyleSheet("#l_marchandise { border: 3px solid red; }")
        else:
            self.mainWidget.ui.l_marchandise.setStyleSheet("")
            
        if to_complete == 0:
            self.accept()
            
    
    @staticmethod
    def commandDelivery(parent, ctr, delivery = None):
        dialog = deliveryEditor(parent, ctr, delivery)
        result = dialog.exec_()
        if result == QtGui.QDialog.Accepted:
            dic = {}
            dic["date_appel"] = datetime.datetime.now().strftime("%d/%m/%Y")
#            dic["date_charg_livr"] = dialog.mainWidget.ui.cb_jour.currentText() + '/' + dialog.mainWidget.ui.cb_date.currentText()
            dic["date_theorique"] = dialog.mainWidget.ui.cb_date.currentText()
            dic["date_charg_livr"] = dialog.mainWidget.ui.d_date_reelle.date().toString("dd/MM/yyyy")
            dic["horaire_charg_livr"] = dialog.mainWidget.ui.l_horaire.text()
            dic["quantite"] = dialog.mainWidget.ui.l_qte.text()
            dic["marchandise"] = dialog.mainWidget.ui.l_marchandise.text()
            dic["ville"] = dialog.mainWidget.ui.cb_ville.itemData( dialog.mainWidget.ui.cb_ville.currentIndex() )
            dic["ref_client"] = dialog.mainWidget.ui.l_ref_client.text()
            dic["ref_fourniss"] = dialog.mainWidget.ui.l_ref_fourniss.text()
            dic["ref_chargement"] = dialog.mainWidget.ui.l_ref_charg.text()
            return dic
        else:
            return None
       
    @staticmethod
    def updateDelivery(parent, ctr, delivery):
        dialog = deliveryEditor(parent, ctr, delivery)
        result = dialog.exec_()
        if result == QtGui.QDialog.Accepted:
#            delivery.date_charg_livr = dialog.mainWidget.ui.cb_jour.currentText()+"/"+dialog.mainWidget.ui.cb_date.currentText()
#            from classes import Livraison
            delivery.date_theorique = dialog.mainWidget.ui.cb_date.currentText()
            delivery.date_charg_livr = dialog.mainWidget.ui.d_date_reelle.date().toString("dd/MM/yyyy")
            delivery.horaire_charg_livr = dialog.mainWidget.ui.l_horaire.text()
            delivery.quantite = dialog.mainWidget.ui.l_qte.text()
            delivery.marchandise = dialog.mainWidget.ui.l_marchandise.text()
            delivery.ville = dialog.mainWidget.ui.cb_ville.itemData( dialog.mainWidget.ui.cb_ville.currentIndex() )
            delivery.ref_client = dialog.mainWidget.ui.l_ref_client.text()
            delivery.ref_fourniss = dialog.mainWidget.ui.l_ref_fourniss.text()
            delivery.ref_chargement = dialog.mainWidget.ui.l_ref_charg.text()
            return delivery
        else:
            return None
    

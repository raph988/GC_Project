# -*- coding: utf-8 -*-
"""
Created on Thu Apr 06 23:22:36 2017

@author: Raph
"""

from PySide import QtCore, QtGui
import sys, datetime


from ui_delivery_manager import Ui_MainWindow as Ui_delivery_manager
from ui_delivery_editor import Ui_ui_delivery_editor as Ui_delivery_editor

from classes import ContractsDatabase
from classes import Market

from parse_excel import ReverseExecutionParser
from utils import number_of_days, format_num

NUM_CTR = 0
NUM_CTR_C = 1
NUM_CTR_F = 2

NUM_DLV_CH = 0
NUM_DLV_C = 1
NUM_DLV_F = 2


class MyTreeWidget(QtGui.QTreeWidget):
    s_dropped_contract = QtCore.Signal(str)
    
    def __init__(self, parent = None):
        super(MyTreeWidget, self).__init__(parent)
        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.setAlternatingRowColors(True)
        self.setIndentation(0)
        self.setDragDropMode(QtGui.QAbstractItemView.DragDrop)
        
    def dragMoveEvent(self, event):
        if event.source() != self:
            event.accept()
        else:
            event.mimeData().setText(self.selectedItems()[0].livr.n_livr)
            event.ignore()
            
    def dropEvent(self, event):
        if event.source() != self:
            n_ctr = event.mimeData().text()
            self.s_dropped_contract.emit(n_ctr)
            event.accept()
        else:
            event.ignore()
            
class TreeWidgetDelivery(QtGui.QTreeWidgetItem):
    def __init__(self, parent, livr, items):
        self.livr = livr
        QtGui.QTreeWidgetItem.__init__(self, parent, items)
          
#        if items[-1] == "Payé":
#            text = "Payé"
#            color = QtGui.QColor(128,255,128)
#        elif items[-1] == "Livré":
#            text = "Livré"
#            color = QtGui.QColor(0,128,255)
#        elif items[-1] == "Confirmé":
#            text = "Confirmé"
#            color = QtGui.QColor(255,255,0)
#        else:
#            text = "En Attente"
#            color = QtGui.QColor(192,192,192)
#        label = QtGui.QLabel(text)
#        label.setObjectName("label_state")
#        label.setStyleSheet("#label_state {background-color : "+color.name()+"; color: black;}")
##        item.setBackground(len(itemlist)-1, color)
#        parent.setItemWidget(self, 13, label)
            
        
class Question(QtGui.QDialog):
    def __init__(self, parent = None, whatIsIt = ""):
#        super(Question, self).__init__(parent)
        QtGui.QDialog.__init__(self, parent)
        
        self.mainLayout = QtGui.QVBoxLayout()
        
        self.label = QtGui.QLabel()
        self.label.setText(whatIsIt.decode('utf-8').strip())
        
        self.buttons = QtGui.QDialogButtonBox( QtGui.QDialogButtonBox.Cancel | QtGui.QDialogButtonBox.Ok, QtCore.Qt.Horizontal, self)
        self.buttons.button(QtGui.QDialogButtonBox.Ok).setText("Valider")
        self.buttons.button(QtGui.QDialogButtonBox.Cancel).setText("Annuler")

        self.mainLayout.addWidget(self.label)
        self.mainLayout.addWidget(self.buttons)
        self.setLayout(self.mainLayout)

        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)

    @staticmethod
    def askNumber(parent = None, whatIsIt = ""):
        dialog = Question(parent, whatIsIt)
        t_number = QtGui.QLineEdit()
        dialog.mainLayout.insertWidget(1, t_number)
        result = dialog.exec_()
        if result == QtGui.QDialog.Accepted:
            return t_number.text()
        else:
            return None
        
    @staticmethod
    def changeState(parent = None, whatIsIt = ""):
        dialog = Question(parent, whatIsIt)
        dialog.buttons.button(QtGui.QDialogButtonBox.Ok).setText("Oui")
        dialog.buttons.button(QtGui.QDialogButtonBox.Cancel).setText("Non")
        result = dialog.exec_()
        if result == QtGui.QDialog.Accepted:
            return True
        else:
            return None
        
    @staticmethod
    def confirmPaiment(parent = None, whatIsIt = ""):
        dialog = Question(parent, whatIsIt)
        layout = QtGui.QHBoxLayout()
        label = QtGui.QLabel("Date du paiement : ")
        w_date = QtGui.QDateEdit()
        w_date.setMinimumDate(QtCore.QDate(2017, 01, 01))
        w_date.setDate(QtCore.QDate.currentDate())
        layout.addWidget(label)
        layout.addWidget(w_date)
        dialog.mainLayout.insertLayout(1, layout)
        result = dialog.exec_()
        if result == QtGui.QDialog.Accepted:
            return w_date.date().toString("dd/MM/yyyy")
        else:
            return None
        
        
        
    @staticmethod
    def warn(parent = None, whatIsIt = ""):
        dialog = Question(parent, whatIsIt)
#        dialog.buttons = QtGui.QDialogButtonBox(QtGui.QDialogButtonBox.Ok, QtCore.Qt.Horizontal, None)
#        dialog.buttons.button( QtGui.QDialogButtonBox.Cancel ).setEnabled( False )
        dialog.buttons.button( QtGui.QDialogButtonBox.Cancel ).hide()
        result = dialog.exec_()
        
        
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
        
        layout = QtGui.QVBoxLayout()
        layout.addWidget(self.mainWidget)
        mainLayout = QtGui.QVBoxLayout()
        mainLayout.addLayout(layout)
        mainLayout.addWidget(self.buttons)
        self.setLayout(mainLayout)

        self.buttons.accepted.connect(self.checkDelivery)
        self.buttons.rejected.connect(self.reject)
        self.mainWidget.ui.cb_date.currentIndexChanged.connect(self.dateSelected)
        
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
        
        if self.ctr.ville is not None and len(self.ctr.ville) > 0:
            self.mainWidget.ui.l_ville.setText(self.ctr.ville)
        else:
            for k, l in sorted(self.ctr.livraisons.items(), key = lambda  x: x[0], reverse = True): # sorted by key/delivery number
                if l.ville is not None and len(l.ville) > 0:
                    self.mainWidget.ui.l_ville.setText(l.ville)
                    break
            
#        self.mainWidget.ui.cb_jour.addItems(list(str(j).zfill(2) for j in range(1, 32, 1)))
#        now = QtCore.QDate.currentDate()
#        self.mainWidget.ui.d_date.setText(str(now.month()) + '/' + str(date.year()))

    def updateWidget(self, delivery):
#        delivery = Livraison()
        if delivery.date_charg_livr is not None:
            date = delivery.date_charg_livr.split('/')
            if len(date) > 2:
                j = date[0]
                m = date[1]
                y = date[2]
            elif len(date) == 0:
                j = '00'
                m = "00"
                y = "0000"
            else:
                j = '00'
                m = date[0]
                y = date[1]
            date = m+"/"+ y
            self.mainWidget.ui.cb_date.setCurrentIndex(self.mainWidget.ui.cb_date.findText(date))
#            self.mainWidget.ui.cb_jour.clear()
#            self.mainWidget.ui.cb_jour.addItems(list(str(j).zfill(2) for j in range(1, number_of_days(m,y)+1, 1)))
            index = self.mainWidget.ui.cb_jour.findText(j.zfill(2))
            if index >= 0:
                self.mainWidget.ui.cb_jour.setCurrentIndex(index)
            else: 
                self.mainWidget.ui.cb_jour.setCurrentIndex(-1)
                
        if delivery.horaire_charg_livr is not None:
            self.mainWidget.ui.l_horaire.setText(delivery.horaire_charg_livr)
        if delivery.marchandise is not None:
            self.mainWidget.ui.l_marchandise.setText(delivery.marchandise)
        if delivery.quantite is not None:
            self.mainWidget.ui.l_qte.setText(delivery.quantite)
        if delivery.ville is not None:
            self.mainWidget.ui.l_ville.setText(delivery.ville)
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
        index = self.mainWidget.ui.cb_jour.currentIndex()
        self.mainWidget.ui.cb_jour.clear()
        self.mainWidget.ui.cb_jour.addItems(list(str(j).zfill(2) for j in range(1, number_of_days(m,y)+1, 1)))
        if index >= self.mainWidget.ui.cb_jour.count() or index < 0:
            self.mainWidget.ui.cb_jour.setCurrentIndex(0)
        else:
            self.mainWidget.ui.cb_jour.setCurrentIndex(index)
        total = format_num(self.ctr.periode_livraison[y][m]["total"])
        done = format_num(self.ctr.periode_livraison[y][m]["done"])
        maximum = format_num(float(total) - float(done) )
        self.mainWidget.ui.l_qte.setPlaceholderText('max: '+maximum)
        
        
    def checkDelivery(self):
        print "checkDelivery"
        to_complete = 0
        if self.mainWidget.ui.cb_jour.currentIndex() < 0:
            to_complete += 1
            self.mainWidget.ui.cb_jour.setStyleSheet("#cb_jour { border: 3px solid red; }")
        else:
            self.mainWidget.ui.cb_jour.setStyleSheet("")
            
        if self.mainWidget.ui.cb_date.currentIndex() < 0:
            to_complete += 1
            self.mainWidget.ui.cb_date.setStyleSheet("#cb_date { border: 3px solid red; }")
        else:
            self.mainWidget.ui.cb_date.setStyleSheet("")
            
        if len(self.mainWidget.ui.l_ville.text()) < 1:
            to_complete += 1
            self.mainWidget.ui.l_ville.setStyleSheet("#l_ville { border: 3px solid red; }")
        else:
            self.mainWidget.ui.l_ville.setStyleSheet("")
            
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
            dic["date_charg_livr"] = dialog.mainWidget.ui.cb_jour.currentText() + '/' + dialog.mainWidget.ui.cb_date.currentText()
            dic["horaire_charg_livr"] = dialog.mainWidget.ui.l_horaire.text()
            dic["quantite"] = dialog.mainWidget.ui.l_qte.text()
            dic["marchandise"] = dialog.mainWidget.ui.l_marchandise.text()
            dic["ville"] = dialog.mainWidget.ui.l_ville.text()
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
            delivery.date_charg_livr = dialog.mainWidget.ui.cb_jour.currentText()+"/"+dialog.mainWidget.ui.cb_date.currentText()
            delivery.horaire_charg_livr = dialog.mainWidget.ui.l_horaire.text()
            delivery.quantite = dialog.mainWidget.ui.l_qte.text()
            delivery.marchandise = dialog.mainWidget.ui.l_marchandise.text()
            delivery.ville = dialog.mainWidget.ui.l_ville.text()
            delivery.ref_client = dialog.mainWidget.ui.l_ref_client.text()
            delivery.ref_fourniss = dialog.mainWidget.ui.l_ref_fourniss.text()
            delivery.ref_chargement = dialog.mainWidget.ui.l_ref_charg.text()
            return delivery
        else:
            return None
    
        
class DeliveryManager(QtGui.QMainWindow, QtCore.QObject):
    
    def __init__(self, parent = None):
        super(DeliveryManager, self).__init__(parent)
        self.ui = Ui_delivery_manager()
        self.ui.setupUi(self)
        
        self.cDB = ContractsDatabase()
        self.comm = self.cDB.communicator
        self.oil_market = Market()
        
        self.comm.s_cDB_updated.connect(self.updateSorters)
        
        self.ui.t_deliver_list.deleteLater()
        self.t_deliver_list = MyTreeWidget(self)
        self.t_deliver_list.setAlternatingRowColors(True)
#        self.ui.t_ctr_list.header().setDefaultAlignment(QtCore.Qt.AlignCenter)
        self.t_deliver_list.setIndentation(0)
        self.t_deliver_list.s_dropped_contract.connect(self.loadDeliveriesFromContract)
        self.t_deliver_list.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.t_deliver_list.customContextMenuRequested.connect(self.customContextMenu)
        self.t_deliver_list.header().setStretchLastSection(True)
#        self.t_deliver_list.header().setResizeMode(QtGui.QHeaderView.Interactive)
        self.t_deliver_list.setDragDropMode(QtGui.QAbstractItemView.DragDrop)
        self.ui.horizontalLayout.addWidget(self.t_deliver_list)
        
        self.ui.l_ref_client.installEventFilter(self)
        self.ui.l_ref_fourniss.installEventFilter(self)
        self.ui.l_ref_charg.installEventFilter(self)
        self.ui.l_ref_client.returnPressed.connect(self.researchDelivery)
        self.ui.l_ref_fourniss.returnPressed.connect(self.researchDelivery)
        self.ui.l_ref_charg.returnPressed.connect(self.researchDelivery)
        self.ui.b_rechercher.clicked.connect(self.researchDelivery)
        self.ui.b_rechercher.setEnabled(False)
        
        self.popMenu = QtGui.QMenu(self)
        self.actionSetConfirm_cmd = QtGui.QAction("Confirmer la demande", self)
        self.actionSetConfirm_cmd.triggered.connect(self.setConfirmation)
        self.actionSetConfirm_dlv = QtGui.QAction("Confirmer la livraison", self)
        self.actionSetConfirm_dlv.triggered.connect(self.setConfirmationLivraison)
        self.actionSetPaied = QtGui.QAction("Confirmer le paiement", self)
        self.actionSetPaied.triggered.connect(self.setPaiment)
        self.actionModifyDeliv = QtGui.QAction("Modifier la livraison", self)
        self.actionModifyDeliv.triggered.connect(self.modifyDelivery)
        self.actionRemove = QtGui.QAction("Supprimer la livraison", self)
        self.actionRemove.triggered.connect(self.removeDelivery)
        self.actionImport = QtGui.QAction("Importer depuis Execution.xlsx", self)
        self.actionImport.triggered.connect(self.importDeliveries)
        
        self.popMenu.addAction(self.actionSetConfirm_cmd)
        self.popMenu.addAction(self.actionSetConfirm_dlv)
        self.popMenu.addAction(self.actionSetPaied)
        self.popMenu.addSeparator()
        self.popMenu.addAction(self.actionModifyDeliv)
        self.popMenu.addSeparator()
        self.popMenu.addAction(self.actionRemove)
        self.popMenu.addSeparator()
        self.popMenu.addAction(self.actionImport)
        
        
        self.popMenu2 = QtGui.QMenu(self)
        self.actionImport2 = QtGui.QAction("Importer depuis Execution.xlsx", self)
        self.actionImport2.triggered.connect(self.importDeliveries)
        self.popMenu2.addAction(self.actionImport)
        
        self.ui.rb_date_appel.setChecked(True)
        self.initDelivList()
        self.initMarchandiseList()
        self.ui.cb_year.currentIndexChanged[int].connect(self.updateDelivList)
        self.ui.rb_date_appel.toggled.connect(self.updateDelivList)
        
        self.ui.cb_month.currentIndexChanged.connect(self.updateDelivList)
        self.ui.cb_sort_client.currentIndexChanged.connect(self.updateDelivList)
        self.ui.cb_sort_fourniss_2.currentIndexChanged.connect(self.updateDelivList)
        self.ui.cb_marchandise.currentIndexChanged.connect(self.updateDelivList)
        self.ui.b_reinit_list.clicked.connect(self.reinitSorters)
        self.updateSorters()
        
        
    
    def eventFilter(self, obj, event):
        if event.type() == QtCore.QEvent.MouseButtonRelease:
            if obj == self.ui.l_ref_charg or obj == self.ui.l_ref_client or obj == self.ui.l_ref_fourniss:
                self.specifyResearch(obj)
                return True
        return False
    
    def customContextMenu(self, pos):
        if self.getSelectedDelivery() is None:
            self.popMenu2.exec_(self.t_deliver_list.mapToGlobal(pos))
        else:
            self.popMenu.exec_(self.t_deliver_list.mapToGlobal(pos))
        
    def initMarchandiseList(self):
        marchandise_list = self.oil_market.marchandises_list['fr']
        ordered_marchandise_list = sorted(marchandise_list)
        zipped = list(enumerate(ordered_marchandise_list))
        
        self.ui.cb_marchandise.blockSignals(True)
        self.ui.cb_marchandise.clear()
        self.ui.cb_marchandise.addItem("- Toutes -", userData = None)
        
        for index, m in zipped:
            self.ui.cb_marchandise.addItem(m, index)
            
        self.ui.cb_marchandise.setCurrentIndex(0)
        self.ui.cb_marchandise.blockSignals(False)
        
        
        
    def initDelivList(self):
        col1 = "Date d'appel".decode('utf-8').strip()
        col2 = "Client".decode('utf-8').strip()
        col3 = "Fournisseur".decode('utf-8').strip()
        col4 = "Départ".decode('utf-8').strip()
        col5 = "Ville".decode('utf-8').strip()
        col6 = "Date de charg/livr".decode('utf-8').strip()
        col7 = "Heure".decode('utf-8').strip()
        col8 = "Quantité".decode('utf-8').strip()
        col9 = "Marchandise".decode('utf-8').strip()
        col10 = "Ctr Giraud".decode('utf-8').strip()
        col11 = "Ctr fournisseur".decode('utf-8').strip()
        col12 = "Réf. client".decode('utf-8').strip()
        col13 = "Réf. chargement".decode('utf-8').strip()
        col14 = "Statut".decode('utf-8').strip()
        
        self.t_deliver_list.setHeaderLabels([col1, col2, col3, col4, col5, col6, col7, col8, col9, col10, col11, col12, col13, col14])
        self.updateDelivList()
        self.t_deliver_list.setSortingEnabled(True)
        self.t_deliver_list.header().setResizeMode(QtGui.QHeaderView.ResizeToContents)

        font = self.t_deliver_list.header().font()
        font.setPointSize(10)
        self.t_deliver_list.header().setFont( font )
        for i in range(0, 14, 1):
            self.t_deliver_list.headerItem().setTextAlignment(i, QtCore.Qt.AlignCenter)

        
    def setConfirmation(self):
        livr_selected = self.getSelectedDelivery()
        if livr_selected is None:
            return 
        ctr = self.cDB.getContractsByNum(livr_selected.n_ctr, NUM_CTR)[0]
        res = (Question.changeState(whatIsIt = "Confirmer la demande de livraison ?"))
        ctr.confirmDelivery(livr_selected, res)
        self.cDB.updateContract(ctr)
        
        
    def setConfirmationLivraison(self):
        livr_selected = self.getSelectedDelivery()
        if livr_selected is None:
            return 
        ctr = self.cDB.getContractsByNum(livr_selected.n_ctr, NUM_CTR)[0]
        res = Question.changeState(whatIsIt = "Confirmer la demande de livraison ?")
        ctr.validateDelivery(livr_selected, res)
        self.cDB.updateContract(ctr)
    
    def setPaiment(self):
        livr_selected = self.getSelectedDelivery()
        if livr_selected is None:
            return 
        ctr = self.cDB.getContractsByNum(livr_selected.n_ctr, NUM_CTR)[0]
        res = Question.confirmPaiment(whatIsIt = "Confirmer le paiement ?")
        if res is None:
            return
        ctr.validatePaiment(livr_selected, res)
        self.cDB.updateContract(ctr)
    
    def modifyDelivery(self):
        livr_selected = self.getSelectedDelivery()
        if livr_selected is None:
            return 
        ctr = self.cDB.getContractsByNum(livr_selected.n_ctr, NUM_CTR)[0]
        dlv = deliveryEditor.updateDelivery(self, ctr, livr_selected)
        if dlv is not None:
            ctr.updateDelivery(dlv)
            self.cDB.updateContract(ctr)
        
#        if dic is not None: 
#            ctr = self.getSelectedContract()
#            ctr.updateDelivery(dic)
#            self.cDB.updateContract(ctr)
        
        
    @QtCore.Slot()
    def removeDelivery(self):
        livr_selected = self.getSelectedDelivery()
        if livr_selected is None:
            return 
        ctr = self.cDB.getContractsByNum(livr_selected.n_ctr, NUM_CTR)[0]
        message = "Êtes-vous sûr de vouloir supprimer définitivement cette livraison ?"
        reply = QtGui.QMessageBox.question(self, 'Attention', message, QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)

        if reply == QtGui.QMessageBox.Yes:
            ctr.removeDelivery(livr_selected)
            message = 'Pensez à supprimer la ligne correspondante du fichier livraisons.'
            QtGui.QMessageBox.question(self,'Attention !' , message, QtGui.QMessageBox.Yes)
            self.cDB.updateContract(ctr)
            
#    from classes import Livraison
    @QtCore.Slot()
    def importDeliveries(self):
        progressDialog = QtGui.QProgressDialog()
        progressDialog.setAutoClose(False)
        progressDialog.setAutoReset(False)
        label = progressDialog.findChildren(QtGui.QLabel)[0]
        label.setFont(QtGui.QFont("Calibri", 12))
        button = progressDialog.findChildren(QtGui.QPushButton)[0]
        button.hide()
        progressBar = progressDialog.findChildren(QtGui.QProgressBar)[0]
        progressBar.hide()
        progressDialog.setWindowTitle(u"Travail en cours...")
        text = u"\n\nImport des livraisons à partir de Execution.xlsx"
        progressDialog.setLabelText(text)
        progressDialog.show()
        QtGui.QApplication.processEvents()
        
        ReverseExecutionParser()
        
        progressDialog.close()
        QtGui.QApplication.processEvents()
        
        
        
    def getSelectedDelivery(self):
        items_selected = self.t_deliver_list.selectedItems()
        if len(items_selected) < 1:
#            self.setButtonEnabled(False)
            return None
        return items_selected[0].livr
    
    def updateSorters(self):
        self.initOrdererClient()
        self.initOrdererFourniss()
        self.initOrdererDate()
        
    def reinitSorters(self):
        self.blockSignals(True)
        self.ui.cb_sort_client.setCurrentIndex(0)
        self.ui.cb_sort_fourniss_2.setCurrentIndex(0)
        self.ui.cb_marchandise.setCurrentIndex(0)
        self.ui.cb_month.setCurrentIndex(0)
        self.ui.cb_year.setCurrentIndex(1)
        self.ui.cb_year.setCurrentIndex(0)
        self.blockSignals(False)
        self.updateDelivList()
        
    def initOrdererDate(self):
        self.ui.cb_month.blockSignals(True)
        self.ui.cb_year.blockSignals(True)
        month_names = ["Janvier", "Février", "Mars", "Avril", "Mai", "Juin", "Juillet", "Août", "Septembre", "Octobre", "Novembre", "Décembre"]
        month_values = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "12"]
        self.ui.cb_month.clear()
        self.ui.cb_month.addItem("Mois", userData = None)
        for n, v in zip(month_names, month_values):
            self.ui.cb_month.addItem(n, userData = v)
        self.ui.cb_month.setCurrentIndex(0)
            
        year_max = 0
        for ctr in self.cDB.getEveryContracts():
            if ctr is None: continue
            for livr in ctr.getDeliveries():
                d = livr.date_charg_livr
                if int(d.split('/')[-1]) > year_max:
                    year_max = int(d.split('/')[-1])
        year_now = datetime.datetime.now().year
        self.ui.cb_year.clear()
        self.ui.cb_year.addItem("Année", userData = None)
        for y in range(year_now, year_max+1, 1):
            self.ui.cb_year.addItem(str(y), userData = str(y))
        self.ui.cb_month.blockSignals(False)
        self.ui.cb_year.blockSignals(False)
        
        index = self.ui.cb_year.findText(str(year_now))
        if index < 0: index = 0
        self.ui.cb_year.setCurrentIndex(index)
    
    def initOrdererClient(self):
        self.ui.cb_sort_client.blockSignals(True)
        self.ui.cb_sort_client.clear()
        self.ui.cb_sort_client.addItem("- Tous -", userData = None)
        client_list = self.oil_market.get_client(is_fournisseur=False)
        client_names = list(c.short_name.encode('utf-8') for c in client_list)
        
        zipped = zip(client_names, client_list)
        ordered_client_list = sorted(zipped, key = lambda client: client[0])
        for n, c in ordered_client_list:
            self.ui.cb_sort_client.addItem(n, c)
            
        self.ui.cb_sort_client.setCurrentIndex(0)
        self.ui.cb_sort_client.blockSignals(False)
        
    def initOrdererFourniss(self):
        self.ui.cb_sort_fourniss_2.blockSignals(True)
        self.ui.cb_sort_fourniss_2.clear()
        self.ui.cb_sort_fourniss_2.addItem("- Tous -", userData = None)
        fourniss_list = self.oil_market.get_client(is_fournisseur=True)
        fourniss_names = list(f.short_name.encode('utf-8') for f in fourniss_list)
        
        zipped = zip(fourniss_names, fourniss_list)
        ordered_fourniss_list = sorted(zipped, key = lambda fourniss: fourniss[0])
        for n, f in ordered_fourniss_list:
            self.ui.cb_sort_fourniss_2.addItem(n, f)
            
        self.ui.cb_sort_fourniss_2.setCurrentIndex(0)
        self.ui.cb_sort_fourniss_2.blockSignals(False)
        
        
        
        
        
    
    def specifyResearch(self, sender):
        if "client" in sender.objectName():
            self.ui.rb_ref_client.setChecked(True)
        elif "fourniss" in sender.objectName():
            self.ui.rb_ref_fourniss.setChecked(True)
        elif "charg" in sender.objectName():
            self.ui.rb_ref_charg.setChecked(True)
        elif "march" in sender.objectName():
            self.ui.rb_marchandise.setChecked(True)
        self.ui.b_rechercher.setEnabled(True)
        
    @QtCore.Slot()
    def researchDelivery(self):
        type_num = None
        if self.ui.rb_ref_client.isChecked():
            num = str(self.ui.l_ref_client.text())
            type_num = NUM_DLV_C
        elif self.ui.rb_ref_fourniss.isChecked():
            num = str(self.ui.l_ref_fourniss.text())
            type_num = NUM_DLV_F
        elif self.ui.rb_ref_charg.isChecked():
            num = str(self.ui.l_ref_charg.text())
            type_num = NUM_DLV_CH
            
        if type_num is not None and len(num) > 0:
            deliv_list = self.cDB.getDeliveryByNum(num.rstrip(), type_num)
            self.updateDelivList(deliv_list)
        else:
            self.updateDelivList()
            
            
        
            
    def sortDeliveryList(self, index = None):
        print "sortDeliveryList"
                
        year = self.ui.cb_year.itemData(self.ui.cb_year.currentIndex())
        month = self.ui.cb_month.itemData(self.ui.cb_month.currentIndex())
        client = self.ui.cb_sort_client.itemData(self.ui.cb_sort_client.currentIndex())
        fourniss = self.ui.cb_sort_fourniss_2.itemData(self.ui.cb_sort_fourniss_2.currentIndex())
        if self.ui.cb_marchandise.currentIndex() <= 0:
            marchandise = None
        else:
            marchandise = self.ui.cb_marchandise.itemText(self.ui.cb_marchandise.currentIndex())
            marchandise = self.oil_market.get_code_from_name(marchandise)
        
        deliv_list = self.cDB.getDeliveries(by_month=month, by_year=year, is_appel_date=self.ui.rb_date_appel.isChecked(), by_client=client, by_fourniss = fourniss, by_marchandise=marchandise)
        return deliv_list 
    
    def updateDelivList(self, deliv_list = None):
        print "updateDelivList"
        
        self.t_deliver_list.clear()
        if deliv_list is None or isinstance(deliv_list, list) == False:
            deliv_list = self.sortDeliveryList()
            
        if deliv_list is None: 
            return
        
        itemlist = []
        cpt = 0
        for deliv in deliv_list:
            if deliv is None:
                itemlist = [' - ', ' - ', ' - ', ' - ', ' - ', ' - ', ' - ', ' - ', ' - ', ' - ', ' - ', ' - ', ' - ']
            else:
                ctr = self.cDB.getContractsByNum(deliv.n_ctr, NUM_CTR)[0]
                if ctr.is_franco : depart = "Départ"
                else: depart = "Franco"
                state = "En attente"
                if deliv.is_confirmed: state = "Confirmé"
                if deliv.is_delivered: state = "Livré"
                if deliv.is_paid: state = "Payé"
                if self.oil_market.marchandiseExist(ctr.marchandise):
                    full_marchandise = self.oil_market.getMarchandiseFullName(ctr.marchandise)
                try:
                    nom_client = ctr.getClientName(shortest=True) + "\n" + ctr.get_uVilleAcheteur()
                    nom_fourniss = ctr.getFournissName(shortest=True) + "\n" + ctr.get_uVilleVendeur()
                    itemlist = [deliv.date_appel, nom_client, nom_fourniss, depart, deliv.ville, deliv.date_charg_livr, deliv.horaire_charg_livr, format_num(deliv.quantite), full_marchandise, deliv.n_ctr, deliv.ref_fourniss, deliv.ref_client, deliv.ref_chargement, state]
                except:
                    continue
            newline = TreeWidgetDelivery(self.t_deliver_list, deliv, itemlist)
            for i in range(0, 14, 1):
                newline.setTextAlignment(i, QtCore.Qt.AlignCenter)
                
            if itemlist[-1] == "Payé":
                text = "Payé"
                color = QtGui.QColor(6, 76, 15)
            elif itemlist[-1] == "Livré":
                text = "Livré"
                color = QtGui.QColor(96, 9, 9)
            elif itemlist[-1] == "Confirmé":
                text = "Confirmé"
                color = QtGui.QColor(0, 0, 0)
            else:
                text = "En Attente"
                color = QtGui.QColor(50,50,50)

            newline.setForeground(len(itemlist)-1, color)
#            newline.setAutoFillBackground(False)
#            newline.setBackground(len(itemlist)-1, color)
#            label = QtGui.QLabel(text)
#            label.setObjectName("label_state")
#            label.setStyleSheet("#label_state {background-color : "+color.name()+"; color: black;}")
#            newline.setBackground(len(itemlist)-1, color)
#            line = self.t_deliver_list.itemFromIndex( cpt )
#            self.t_deliver_list.setItemWidget(line, 13, label)
            cpt += 1
            
        self.t_deliver_list.header().setResizeMode(QtGui.QHeaderView.ResizeToContents)
        self.t_deliver_list.header().setResizeMode(QtGui.QHeaderView.Interactive)
        self.t_deliver_list.setAutoFillBackground(False)
        for i in range(0, len(itemlist), 1):
            self.t_deliver_list.resizeColumnToContents(i)
            
#        model = self.t_deliver_list.selectionModel()
#        indexList = model.selectedIndexes()
#        line = self.t_deliver_list.itemFromIndex( indexList[cpt] )
#        text = line.data(indexList[cpt].column(), QtGui.Qt.DisplayRole).toString()
#        if text == "Payé":
#            color = QtGui.QColor(128,255,128)
#        elif text == "Livré":
#            color = QtGui.QColor(0,128,255)
#        elif text == "Confirmé":
#            color = QtGui.QColor(255,255,0)
#        else:
#            color = QtGui.QColor(192,192,192)
#        label = QtGui.QLabel(text)
#        label.setObjectName("label_state")

#         TreeWidgetItem->setBackgroundColor(col, QColor(255, 255, 0, 100))
#        item.setForeground(len(itemlist)-1, color)
            
#        self.t_deliver_list.header().setResizeMode(self.t_deliver_list.columnCount()-3, QtGui.QHeaderView.Stretch)
        self.repaint()
        
    @QtCore.Slot(str)
    def loadDeliveriesFromContract(self, n_ctr):
        ctr = self.cDB.getContractsByNum(n_ctr, NUM_CTR)[0]
#        dlv = Contract.livraisons
        dlv_list = list(l for n, l in ctr.livraisons.items())
        self.updateDelivList(dlv_list)
        
    def main(self):
        self.show()
      
        
if __name__ == "__main__":

    app = QtGui.QApplication(sys.argv)
    cc = DeliveryManager()
    cc.main()
    sys.exit(app.exec_())
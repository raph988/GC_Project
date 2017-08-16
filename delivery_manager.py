# -*- coding: utf-8 -*-
"""
Created on Thu Apr 06 23:22:36 2017

@author: Raph
"""

from PySide import QtCore, QtGui
import sys, datetime
import inspect, re
from PIL import ImageFont

from ui_delivery_manager import Ui_MainWindow as Ui_delivery_manager

from delivery_editor import deliveryEditor
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
        self.parent = parent
        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.setAlternatingRowColors(True)
        self.setIndentation(0)
        self.setDragDropMode(QtGui.QAbstractItemView.DragDrop)
        self.setDefaultDropAction(QtCore.Qt.CopyAction)
        
    def dragMoveEvent(self, event):
        if event.source() != self:
            event.accept()
        else:
            item_selected = self.selectedItems()[0]
            event.mimeData().setText(item_selected.livr.n_livr)
            
            html = "<table><tr>"
            for i in range( 0, item_selected.columnCount(), 1):
                text = item_selected.text(i)
                if i != 8:
                    text = text.replace('\n','<br/>')
                html += "<td>"+text+"</td>"
            html += "</tr></table>"
            event.mimeData().setHtml(html)
            
            event.accept()
            
            
#    def mouseReleaseEvent(self, event):
#        print "MyTreeWidget mouseReleaseEvent"
#        self.parent.updateDelivList()
            
    def dropEvent(self, event):
        print "deliv drop event"
        if event.source() != self:
            n_ctr = event.mimeData().text()
            self.s_dropped_contract.emit(n_ctr)
            event.accept()
#            event.source().updateCtrList()
        else:
            event.ignore()
        
        
class TreeWidgetItemLabel(QtGui.QWidget):
    def __init__(self, parent=None, text=""):
        super(TreeWidgetItemLabel, self).__init__(parent)
        mainLayout = QtGui.QVBoxLayout()
        self.myLabel = QtGui.QLabel()
        self.myLabel.setObjectName("label_state")
        self.myLabel.setText("<span>"+text+"</span>")
        self.myLabel.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignCenter)
        self.setAttribute(QtCore.Qt.WA_TransparentForMouseEvents)
        
        try:
            if "pay" in text.lower():
                color = QtGui.QColor(0, 255, 40)
            elif "confirm" in text.lower():
                color = QtGui.QColor(255, 238, 0)
            elif "attente" in text.lower():
                color = QtGui.QColor(255,0,0)
            else:
                self.myLabel.setObjectName("")
                color = QtGui.QColor(255,0,0)
        except:
            color = QtGui.QColor(255,0,0)
            
        self.myLabel.setStyleSheet("#label_state {background-color : "+color.name()+"; color: black;}")
        mainLayout.addWidget(self.myLabel)
        self.setLayout(mainLayout)



class TreeWidgetDelivery(QtGui.QTreeWidgetItem):
    def __init__(self, parent, livr, items):
        self.livr = livr
        QtGui.QTreeWidgetItem.__init__(self, parent, items)
          
    def __lt__(self, otherItem):
        column = self.treeWidget().sortColumn()
        try:
            return datetime.datetime.strptime(self.text(column), "%d/%m/%Y").toordinal() > datetime.datetime.strptime(otherItem.text(column), "%d/%m/%Y").toordinal()
        except ValueError:
            return self.text(column) > otherItem.text(column)
            
        
class Question(QtGui.QDialog):
    def __init__(self, parent = None, whatIsIt = ""):
        super(Question, self).__init__(parent)
#        QtGui.QDialog.__init__(self, parent)
        
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
    def changeState(parent = None, whatIsIt = "", button_1 = "Oui", button_2 = "Non"):
        dialog = Question(parent, whatIsIt)
        dialog.buttons.button(QtGui.QDialogButtonBox.Ok).setText(button_1)
        dialog.buttons.button(QtGui.QDialogButtonBox.Cancel).setText(button_2)
        result = dialog.exec_()
        if result == QtGui.QDialog.Accepted:
            return True
        else:
            return False
        
    @staticmethod
    def confirmPaiment(parent = None, whatIsIt = "", button_1 = "Oui", button_2 = "Non"):
        dialog = Question(parent, whatIsIt)
        dialog.buttons.button(QtGui.QDialogButtonBox.Ok).setText(button_1)
        dialog.buttons.button(QtGui.QDialogButtonBox.Cancel).setText(button_2)
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
        dialog.exec_()
        
       
class DeliveryManager(QtGui.QMainWindow, QtCore.QObject):
    
    def __init__(self, parent = None):
        super(DeliveryManager, self).__init__(parent)
        self.ui = Ui_delivery_manager()
        self.ui.setupUi(self)
        
        self.cDB = ContractsDatabase()
        self.comm = self.cDB.communicator
        self.oil_market = Market()
        
        
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
        self.ui.t_deliv_tot.setIndentation(0)
        
        self.ui.l_ref_client.installEventFilter(self)
        self.ui.l_ref_fourniss.installEventFilter(self)
        self.ui.l_ref_charg.installEventFilter(self)
        self.ui.l_ref_client.returnPressed.connect(self.researchDelivery)
        self.ui.l_ref_fourniss.returnPressed.connect(self.researchDelivery)
        self.ui.l_ref_charg.returnPressed.connect(self.researchDelivery)
        self.ui.b_rechercher.clicked.connect(self.researchDelivery)
        self.ui.b_rechercher.setEnabled(False)
        
        self.popMenu = QtGui.QMenu(self)
        self.actionSetConfirm_dlv = QtGui.QAction("Confirmer/infirmer la livraison", self)
        self.actionSetConfirm_dlv.triggered.connect(self.setConfirmationLivraison)
        self.actionSetPaied = QtGui.QAction("Confirmer/infirmer le paiement", self)
        self.actionSetPaied.triggered.connect(self.setPaiment)
        self.actionModifyDeliv = QtGui.QAction("Modifier la livraison", self)
        self.actionModifyDeliv.triggered.connect(self.modifyDelivery)
        self.actionRemove = QtGui.QAction("Supprimer la livraison", self)
        self.actionRemove.triggered.connect(self.removeDelivery)
        self.actionImport = QtGui.QAction("Importer des livraisons depuis Execution.xlsx", self)
        self.actionImport.triggered.connect(self.importDeliveries)
        
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
        
        self.ui.cb_marchandise.view().setAlternatingRowColors(True)
        self.ui.cb_sort_client.view().setAlternatingRowColors(True)
        self.ui.cb_sort_fourniss_2.view().setAlternatingRowColors(True)
        
        self.ui.rb_date_appel.setChecked(True)
        self.initMarchandiseList()
        self.initOrdererClient()
        self.initOrdererFourniss()
        self.initOrdererDate()
        self.initDelivList()
        
        self.t_deliver_list.itemSelectionChanged.connect(self.itemSelected)
        self.ui.cb_year.currentIndexChanged.connect(self.updateDelivList)
        self.ui.rb_date_appel.toggled.connect(self.updateDelivList)
        
        self.ui.cb_month.currentIndexChanged.connect(self.updateDelivList)
        self.ui.cb_sort_client.currentIndexChanged.connect(self.updateDelivList)
        self.ui.cb_sort_fourniss_2.currentIndexChanged.connect(self.updateDelivList)
        self.ui.cb_marchandise.currentIndexChanged.connect(self.updateDelivList)
        self.ui.b_reinit_list.clicked.connect(self.reinitSorters)
        self.comm.s_cDB_updated.connect(self.updateSorters)
        
        
    def eventFilter(self, obj, event):
        try:
            if event.type() == QtCore.QEvent.MouseButtonRelease:
                if obj == self.ui.l_ref_charg or obj == self.ui.l_ref_client or obj == self.ui.l_ref_fourniss:
                    self.specifyResearch(obj)
                    return True
        except: pass
        return False
    
    @QtCore.Slot()
    def itemSelected(self):
#        modifiers = QtGui.QApplication.keyboardModifiers()
#        if modifiers == QtCore.Qt.ControlModifier:
#            self.t_deliver_list.setSelectionMode( QtGui.QAbstractItemView.MultiSelection ) 
#        else:
#            self.t_deliver_list.setSelectionMode( QtGui.QAbstractItemView.SingleSelection ) 
        pass
            
            
    def customContextMenu(self, pos):
        if self.getSelectedDelivery() is None:
            self.popMenu2.exec_(self.t_deliver_list.mapToGlobal(pos))
        else:
            self.popMenu.exec_(self.t_deliver_list.mapToGlobal(pos))
        
        
        
        
    def initMarchandiseList(self):
        self.ui.cb_marchandise.blockSignals(True)
        marchandise_list = self.oil_market.marchandises_list['fr']
        ordered_marchandise_list = sorted(marchandise_list)
        zipped = list(enumerate(ordered_marchandise_list))
        
        self.ui.cb_marchandise.clear()
        self.ui.cb_marchandise.addItem("- Toutes -", userData = None)
        
        for index, m in zipped:
            self.ui.cb_marchandise.addItem(m, index)
            
        self.ui.cb_marchandise.setCurrentIndex(0)
        self.ui.cb_marchandise.blockSignals(False)
        
        
        
    def initDelivList(self):
        font = self.t_deliver_list.header().font()
        font.setPointSize(10)
        
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
        headers = [col1, col2, col3, col4, col5, col6, col7, col8, col9, col10, col11, col12, col13, col14]
        self.t_deliver_list.setHeaderLabels(headers)
        self.t_deliver_list.setSortingEnabled(True)
        self.t_deliver_list.header().setFont( font )
        for i in range(0, len(headers), 1):
            self.t_deliver_list.headerItem().setTextAlignment(i, QtCore.Qt.AlignCenter)

        col1 = "Qte totale (T)".decode('utf-8').strip()
        col2 = "Qte à livrer (T)".decode('utf-8').strip()
        headers = [col1, col2]
        self.ui.t_deliv_tot.setHeaderLabels(headers)
        self.ui.t_deliv_tot.setSortingEnabled(True)
        self.ui.t_deliv_tot.header().setFont( font )
        width = self.ui.t_deliv_tot.parent().sizeHint().width()
        for i in range(0, len(headers), 1):
            self.ui.t_deliv_tot.headerItem().setTextAlignment(i, QtCore.Qt.AlignCenter)
            self.ui.t_deliv_tot.header().resizeSection(i, width/3)
        self.ui.t_deliv_tot.header().setStretchLastSection(True)
        
        self.updateDelivList()
        self.t_deliver_list.header().setResizeMode(QtGui.QHeaderView.ResizeToContents)
        self.t_deliver_list.header().setResizeMode(QtGui.QHeaderView.Interactive)
              
        
    def setConfirmationLivraison(self):
        livr_selected = self.getSelectedDelivery()
        if livr_selected is None:
            return 
        error_occured = 0
        ctr = self.cDB.getContractByNum(livr_selected.n_ctr)
        res = Question.changeState(whatIsIt = "À propos de la livraison :", button_1="Confimer", button_2="Déconfirmer")
        res = ctr.confirmDelivery(livr_selected, res)
        if res is None or res == 0:
            if self.cDB.updateContract(ctr) < 0:
                ctr.confirmDelivery(livr_selected, not res)
                error_occured += 1
        else:
            error_occured += 1
            
        if error_occured > 0:
            Question.warn(whatIsIt = "Erreur lors de l'édition de Execution \nVeuillez reessayer ultérieurement...")
            
    
    def setPaiment(self):
        livr_selected = self.getSelectedDelivery()
        if livr_selected is None:
            return 
        
        error_occured = 0
        ctr = self.cDB.getContractByNum(livr_selected.n_ctr)
        res = Question.confirmPaiment(whatIsIt = "À propos du paiement :", button_1="Confimer", button_2="Déconfirmer")
        res = ctr.validatePaiment(livr_selected, res)
        if res is None or res == 0:
            if self.cDB.updateContract(ctr) < 0:
                ctr.validatePaiment(livr_selected, res)
                error_occured += 1
        else:
            error_occured += 1
            
        if error_occured > 0:
            Question.warn(whatIsIt = "Erreur lors de l'édition de Execution \nVeuillez reessayer ultérieurement...")
    
    
    def addDelivery(self, ctr):
        if ctr is None:
            return 
        error_occured = 0
        dic = deliveryEditor.commandDelivery(self, ctr)
        if dic is not None: 
            res, newDeliv = ctr.newDelivery(dic)
            if res == 0: # tout va bien
                if self.cDB.updateContract(ctr) < 0:
                    error_occured += 1
            else: error_occured += 1
        
        if error_occured > 0:
            Question.warn(whatIsIt = "Erreur lors de l'édition de Execution \nVeuillez reessayer ultérieurement...")
            self.modifyDelivery(newDeliv)
            
                
    
    
    def modifyDelivery(self, dlv=None):
        checkDlvNumber = False
        if dlv is None:
            dlv = self.getSelectedDelivery()
        else:
            checkDlvNumber = True
            
        if dlv is None:
            return 
        
        ctr = self.cDB.getContractByNum(dlv.n_ctr)
        if checkDlvNumber:
            dlv = ctr.checkKey(dlv)
            
        error_occured = 0
        dlv = deliveryEditor.updateDelivery(self, ctr, dlv)
        if dlv is not None:
            res = ctr.updateDelivery(dlv)
            if res is None:
                if self.cDB.updateContract(ctr, wait=True) < 0:
                    error_occured += 1
            else: error_occured += 1
                    
        if error_occured > 0:
                Question.warn(whatIsIt = "Erreur lors de l'édition de Execution \nVeuillez reessayer ultérieurement...")
                self.modifyDelivery(dlv)
        
        
        
        
    @QtCore.Slot()
    def removeDelivery(self):
        livr_selected = self.getSelectedDelivery()
        if livr_selected is None:
            return 
        ctr = self.cDB.getContractsByNum(livr_selected.n_ctr, NUM_CTR)[0]
        message = "Êtes-vous sûr de vouloir supprimer définitivement cette livraison ?"
        reply = QtGui.QMessageBox.question(self, 'Attention', message, QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)

        if reply == QtGui.QMessageBox.Yes:
            res = ctr.removeDelivery(livr_selected)
            if res is None or res == 0:
                self.cDB.updateContract(ctr)
            else:
                Question.warn(whatIsIt = "Veuillez reessayer ultérieurement...\nErreur lors de l'édition de Execution.xlsx.")
            
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
        
        if ReverseExecutionParser() < 0:
            Question.warn(whatIsIt = "Veuillez reessayer ultérieurement...\nErreur lors de l'édition de Execution.xlsx.")
            
        
        progressDialog.close()
        QtGui.QApplication.processEvents()
        
        
        
    def getSelectedDelivery(self):
        items_selected = self.t_deliver_list.selectedItems()
        if len(items_selected) < 1:
#            self.setButtonEnabled(False)
            return None
        return items_selected[0].livr
    
    def updateSorters(self):
        self.initOrdererDate()
        self.updateDelivList()
        
    def reinitSorters(self):
        self.ui.cb_sort_client.blockSignals(True)
        self.ui.cb_sort_fourniss_2.blockSignals(True)
        self.ui.cb_marchandise.blockSignals(True)
        self.ui.cb_month.blockSignals(True)
        self.ui.cb_year.blockSignals(True)
        self.ui.cb_sort_client.setCurrentIndex(0)
        self.ui.cb_sort_fourniss_2.setCurrentIndex(0)
        self.ui.cb_marchandise.setCurrentIndex(0)
        self.ui.cb_month.setCurrentIndex(0)
        self.ui.cb_year.setCurrentIndex(0)
        self.ui.cb_sort_client.blockSignals(False)
        self.ui.cb_sort_fourniss_2.blockSignals(False)
        self.ui.cb_marchandise.blockSignals(False)
        self.ui.cb_month.blockSignals(False)
        self.ui.cb_year.blockSignals(False)
        self.updateDelivList()
        
    def initOrdererDate(self):
        try:
            sender = self.sender()
            print "initOrdererDate from "+sender.objectName()
        except:
            curframe = inspect.currentframe()
            calframe = inspect.getouterframes(curframe, 2)
            print "initOrdererDate called by ", calframe[1][3]
            
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
        
        index = self.ui.cb_year.findText(str(year_now))
        if index < 0: index = 0
        self.ui.cb_year.setCurrentIndex(index)

        self.ui.cb_month.blockSignals(False)
        self.ui.cb_year.blockSignals(False)
        print "end of initOrdererDate"
        
    
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
        
        curframe = inspect.currentframe()
        calframe = inspect.getouterframes(curframe, 1)
        print "updateDelivList called by ", calframe[1][3]
        
        self.t_deliver_list.clear()
        if deliv_list is None or isinstance(deliv_list, list) == False:
            deliv_list = self.sortDeliveryList()
            
        if deliv_list is None: 
            return
        
        font = ImageFont.truetype('times.ttf', 12)
        itemlist = []
        for deliv in deliv_list:
            if deliv is None:
                itemlist = [' - ', ' - ', ' - ', ' - ', ' - ', ' - ', ' - ', ' - ', ' - ', ' - ', ' - ', ' - ', ' - ']
            else:
                
                ctr = self.cDB.getContractByNum(deliv.n_ctr)
                if ctr.is_franco : depart = "Franco"
                else: depart = "Départ"
                state = "En attente"
                if deliv.is_confirmed: state = "Confirmé"
                if deliv.is_paid: state = "Payé"
                if self.oil_market.marchandiseExist(ctr.marchandise):
                    full_marchandise = self.oil_market.getMarchandiseFullName(ctr.marchandise)
                    string = ""
                    current_size = 0
                    for word in full_marchandise.split(' '):
                        current_size += font.getsize(word)[0]
                        if current_size > 80:
                            string += "<br/>"
                            current_size = 0
                        string += word + ' '
                    full_marchandise = string
                else:
                    full_marchandise = ""
                
                nom_client = ctr.getClientName(shortest=True).upper() + "<br/>" +"<i>"+ ctr.get_uVilleAcheteur() + "</i>"
                nom_fourniss = ctr.getFournissName(shortest=True).upper() + "<br/>" +"<i>"+ ctr.get_uVilleVendeur()+ "</i>"
            
                itemlist = [deliv.date_appel, nom_client, nom_fourniss, depart, deliv.ville, deliv.date_charg_livr, deliv.horaire_charg_livr, format_num(deliv.quantite), full_marchandise, deliv.n_ctr, deliv.ref_fourniss, deliv.ref_client, deliv.ref_chargement, state]

            blankItemlist = list(re.sub(r"<[^>]*>",r'', s.replace("<br/>", '\n')) for s in itemlist)
            newline = TreeWidgetDelivery(self.t_deliver_list, deliv, blankItemlist)
            
            for i in range(0, len(itemlist)):
                item = itemlist[i]
                self.t_deliver_list.setItemWidget(newline, i, TreeWidgetItemLabel(self, item))
            
            
        self.t_deliver_list.header().setResizeMode(QtGui.QHeaderView.ResizeToContents)
        self.t_deliver_list.header().setResizeMode(QtGui.QHeaderView.Interactive)
        self.t_deliver_list.setAutoFillBackground(False)
        for i in range(0, len(itemlist), 1):
            self.t_deliver_list.resizeColumnToContents(i)
   
#        self.t_deliver_list.header().setResizeMode(self.t_deliver_list.columnCount()-3, QtGui.QHeaderView.Stretch)
        self.updateTotal(deliv_list)
        
    
    def updateTotal(self, deliv_list):
        qte_totale = 0.0
        
        self.ui.t_deliv_tot.clear()
        for deliv in deliv_list:
            qte_totale += float(format_num(deliv.quantite))
            
        qte_a_livrer = qte_totale
        for deliv in deliv_list:
            if deliv.is_confirmed:
                qte_a_livrer -= float(format_num(deliv.quantite))
                
        
        
        newLine = QtGui.QTreeWidgetItem(self.ui.t_deliv_tot, [""]*2)
        self.ui.t_deliv_tot.setItemWidget(newLine, 0, TreeWidgetItemLabel(self, str(qte_totale)))
        self.ui.t_deliv_tot.setItemWidget(newLine, 1, TreeWidgetItemLabel(self, str(qte_a_livrer)))
        
        height = self.ui.t_deliv_tot.visualItemRect(newLine).height()
        width = self.ui.t_deliv_tot.parent().sizeHint().width()
        self.ui.t_deliv_tot.setFixedHeight(height*2)
        self.ui.t_deliv_tot.header().resizeSection(0, width/3)
        self.ui.t_deliv_tot.header().resizeSection(1, width/3)
        
    @QtCore.Slot(str)
    def loadDeliveriesFromContract(self,ctr):
        ctr = self.cDB.getContractsByNum(ctr, NUM_CTR)[0]
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
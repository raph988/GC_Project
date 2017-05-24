# -*- coding: utf-8 -*-
"""
Created on Thu Mar 30 08:46:55 2017

@author: Raph
"""


from PySide import QtCore, QtGui
from sys import maxint
import datetime

import win32com.client as wc
from os import listdir, startfile
from os.path import join, exists
import threading

from ui_contracts_manager import Ui_modif_contract as Ui_ContractsManager
from delivery_manager import deliveryEditor
from contract_initer import ContractIniter
from contract_editor import ContractEditor
from pdf_creator import PDFCreator

from utils import getFromConfig
from utils import mathTex_to_QPixmap, format_num

from classes import ContractsDatabase
from classes import Market

NUM_CTR = 0
NUM_CTR_C = 1
NUM_CTR_F = 2


class MyTreeWidget(QtGui.QTreeWidget):
    s_dropped_delivery = QtCore.Signal(str)
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
            ctr_selected = self.selectedItems()[0]
            if ctr_selected.ctr is not None:
                n_ctr = ctr_selected.ctr.n_contrat
            else:
                n_ctr = ctr_selected.n_ctr
            event.mimeData().setText(n_ctr)
            event.ignore()
    def dropEvent(self, event):
        if event.source() != self:
            n_livr = event.mimeData().text()
            self.s_dropped_delivery.emit(n_livr)
            event.accept()
        else:
            event.ignore()

class TreeWidgetContract(QtGui.QTreeWidgetItem):
    def __init__(self, parent, ctr, items, n_ctr = None):
        self.ctr = ctr
        if ctr is None:
            self.n_ctr = n_ctr
        else:
            self.n_ctr = ctr.n_contrat
        QtGui.QTreeWidgetItem.__init__(self, parent, items)


class Question(QtGui.QDialog):
    def __init__(self, parent = None, whatIsIt = ""):
        super(Question, self).__init__(parent)
#        QtGui.QDialog.__init__(self, parent)
        
        self.mainLayout = QtGui.QVBoxLayout()
        self.layout = QtGui.QHBoxLayout()
        
        self.t_number = QtGui.QLineEdit()
        
        self.label = QtGui.QLabel()
        self.label.setText(whatIsIt.decode('utf-8').strip())
        
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.t_number)
        
        self.buttons = QtGui.QDialogButtonBox( QtGui.QDialogButtonBox.Cancel | QtGui.QDialogButtonBox.Ok, QtCore.Qt.Horizontal, self)
        self.buttons.button(QtGui.QDialogButtonBox.Ok).setText("Valider")
        self.buttons.button(QtGui.QDialogButtonBox.Cancel).setText("Annuler")
        
        self.mainLayout.addLayout(self.layout)
        self.mainLayout.addWidget(self.buttons)
        self.setLayout(self.mainLayout)

        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)

    @staticmethod
    def askNumber(parent = None, whatIsIt = ""):
        dialog = Question(parent, whatIsIt)
        result = dialog.exec_()
        if result == QtGui.QDialog.Accepted:
            return dialog.t_number.text()
        else:
            return None

class DeliveriesViewer(QtGui.QWidget):
    
    def __init__(self, parent=None, ctr=None):
        super(DeliveriesViewer, self).__init__(parent)
        if ctr is None: return
        
        self.setObjectName("calendar_dlv")
        self.month_values = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]
        dlv_list = ctr.periode_livraison
        
        n_years = len(dlv_list.keys())
        self.tableWidget = QtGui.QTableWidget(n_years, len(self.month_values))
        self.tableWidget.setSelectionMode(QtGui.QAbstractItemView.NoSelection)
        self.tableWidget.setFocusPolicy(QtCore.Qt.NoFocus)
        self.tableWidget.setShowGrid(True)
        
        ordered_years = sorted(dlv_list.keys())
        self.tableWidget.setVerticalHeaderLabels(ordered_years)
        self.tableWidget.setHorizontalHeaderLabels(self.month_values)
        
        self.tableWidget.resizeColumnsToContents()
        self.tableWidget.setFixedSize(self.tableWidget.horizontalHeader().length() + 50, self.tableWidget.verticalHeader().length() + 40)
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.tableWidget.verticalHeader().setStretchLastSection(True)
        
        mainLayout = QtGui.QVBoxLayout()
        mainLayout.addWidget(self.tableWidget)
        self.setLayout(mainLayout)
        self.updateGrid(dlv_list)


    def updateGrid(self, dlv_list):
        ordered_years = sorted(dlv_list.keys())
        for i in range(0, len(ordered_years), 1):
            y = ordered_years[i]
            for j in range(0, len(self.month_values)):
                m = self.month_values[j]
                self.tableWidget.setItem(i, j, QtGui.QTableWidgetItem())
                
                total = format_num(dlv_list[y][m]["total"])
                delivered = format_num(dlv_list[y][m]["done"])
                if float(total) == 0:
                    q = '$'+delivered+'$'
                    p_size = 12
                else:
                    q = '$\\frac{'+delivered+'}{'+total+'}$'
                    p_size = 14
                pixmap = mathTex_to_QPixmap(q, p_size)
                
                widget = QtGui.QWidget()
                layout = QtGui.QHBoxLayout()
                label = QtGui.QLabel()
                label.setMaximumSize(QtCore.QSize(32, 32))
                label.setScaledContents(True)
                label.setPixmap(pixmap)
                layout.addWidget(label)
                layout.setAlignment(QtCore.Qt.AlignCenter)
                layout.setContentsMargins(0,5,0,0)
                widget.setLayout(layout)
                self.tableWidget.setCellWidget(i, j, widget)
                if float(total) > float(delivered):
                    self.tableWidget.item(i,j).setBackground(QtGui.QColor(245, 247, 170))
                elif float(total) == float(delivered):
                    self.tableWidget.item(i,j).setBackground(QtGui.QColor(179, 255, 170))
                elif float(total) < float(delivered):
                    self.tableWidget.item(i,j).setBackground(QtGui.QColor(255, 170, 170))
                
        self.tableWidget.resizeRowsToContents()
        self.tableWidget.resizeColumnsToContents()
        
        

class ContractsManager(QtGui.QMainWindow, QtCore.QObject):
    
    def __init__(self, parent = None):
        super(ContractsManager, self).__init__(parent)
        self.ui = Ui_ContractsManager()
        self.ui.setupUi(self)
        
        self.cDB = ContractsDatabase()
        self.comm = self.cDB.communicator
        self.oil_market = Market()
        
        self.ui.t_ctr_list.deleteLater()
        self.t_ctr_list = MyTreeWidget(self)
        self.t_ctr_list.setObjectName("t_ctr_list")
        self.ui.horizontalLayout.addWidget(self.t_ctr_list)
        self.t_ctr_list.itemSelectionChanged.connect(self.itemSelected)
        self.t_ctr_list.customContextMenuRequested.connect(self.customContextMenu)
        self.t_ctr_list.s_dropped_delivery.connect(self.loadContractFromDeliveries)
        self.initCtrList()
        self.initOrdererMarchandise()
        
        self.ui.cb_marchandise.currentIndexChanged[int].connect(self.updateCtrList)
        self.ui.cb_sort_year.currentIndexChanged.connect(self.updateCtrList)
        self.updateSorters()
        self.ui.cb_sort_client_2.currentIndexChanged.connect(self.updateCtrList)
        self.ui.cb_sort_fourniss.currentIndexChanged.connect(self.updateCtrList)
        self.ui.b_reinit_list.clicked.connect(self.reinitSorters)
        
#        self.comm.s_cDB_updated.connect(self.updateCtrList)
        self.comm.s_cDB_updated.connect(self.updateSorters)
        
        self.printer = PDFCreator(self)
        self.printer.setAttribute(QtCore.Qt.WA_StyledBackground)
        
        
        self.popMenu = QtGui.QMenu(self)
        self.actionPDF = QtGui.QAction("Voir le contrat", self)
        self.actionPDF.triggered.connect(self.openPdfContract)
        self.actionAddNumberC = QtGui.QAction("Ajouter numero client", self)
        self.actionAddNumberC.triggered.connect(self.setClientNumber)
        self.actionAddNumberF = QtGui.QAction("Ajouter numero fournisseur", self)
        self.actionAddNumberF.triggered.connect(self.setFournissNumber)
        self.actionAddDelivery = QtGui.QAction("Nouvelle livraison", self)
        self.actionAddDelivery.triggered.connect(self.addDelivery)
        self.actionRemoveCtr = QtGui.QAction("Supprimer le contrat", self)
        self.actionRemoveCtr.triggered.connect(self.removeContract)
        self.actionModifyCtr = QtGui.QAction("Modifier le contrat", self)
        self.actionModifyCtr.triggered.connect(self.modifyContract)
        self.actionAccessToClient = QtGui.QAction("Fiche client", self)
        self.actionAccessToClient.triggered.connect(self.openClientFile)
        self.actionAccessToFournis = QtGui.QAction("Fiche fournisseur", self)
        self.actionAccessToFournis.triggered.connect(self.openFournisFile)
        self.actionPrint = QtGui.QAction("Imprimer le contrat", self)
        self.actionPrint.triggered.connect(self.printContract)
        
        self.popMenu.addAction(self.actionAddDelivery)
        self.popMenu.addSeparator()
        self.popMenu.addAction(self.actionPDF)
        self.popMenu.addAction(self.actionPrint)
        self.popMenu.addAction(self.actionModifyCtr)
        self.popMenu.addSeparator()
        self.popMenu.addAction(self.actionAccessToClient)
        self.popMenu.addAction(self.actionAccessToFournis)
        self.popMenu.addSeparator()
        self.popMenu.addAction(self.actionAddNumberC)
        self.popMenu.addAction(self.actionAddNumberF)
        self.popMenu.addSeparator()
        self.popMenu.addAction(self.actionRemoveCtr)
        
        self.ui.l_n_client.installEventFilter(self)
        self.ui.l_n_ctr.installEventFilter(self)
        self.ui.l_n_fourniss.installEventFilter(self)
        self.ui.l_n_ctr.returnPressed.connect(self.researchContract)
        self.ui.l_n_client.returnPressed.connect(self.researchContract)
        self.ui.l_n_fourniss.returnPressed.connect(self.researchContract)
        
        self.ui.b_rechercher.clicked.connect(self.researchContract)
        self.ui.b_rechercher.setEnabled(False)
        
        self.ui.b_new_contract.clicked.connect(self.newContract)
        
        
    def eventFilter(self, obj, event):
        if event.type() == QtCore.QEvent.MouseButtonRelease:
            if obj == self.ui.l_n_client or obj == self.ui.l_n_ctr or obj == self.ui.l_n_fourniss:
                self.specifyResearch(obj)
                return True
        return False

    def customContextMenu(self, pos):
        self.popMenu.exec_(self.t_ctr_list.mapToGlobal(pos))
        
    @QtCore.Slot()
    def updateSorters(self):
        self.updateOrdererClient()
        self.updateOrdererFourniss()
        self.updateOrdererYear()
        
    def reinitSorters(self):
        self.blockSignals(True)
        self.ui.cb_sort_client_2.setCurrentIndex(0)
        self.ui.cb_sort_fourniss.setCurrentIndex(0)
        self.ui.cb_marchandise.setCurrentIndex(0)
        self.ui.cb_sort_year.setCurrentIndex(0)
        self.blockSignals(False)
        self.updateCtrList()
        
    @QtCore.Slot()
    def openPdfContract(self):
        contract_selected = self.getSelectedContract()
        if contract_selected is not None:
            ctr_path = getFromConfig("path", "data_dir")+"Contrats/"
            file_name = contract_selected.n_contrat + ".pdf"
            ctr_pdf = ""
            for f in listdir(ctr_path):
                if f.endswith(file_name):
                    ctr_pdf = join(ctr_path, file_name)
                    break
            if ctr_pdf == "":
                self.popupMessage("Contrat introuvable ou non édité...")
            else:
                startfile(ctr_pdf)
        else:
            self.popupMessage("Pb avec le contrat...")
        
    
    @QtCore.Slot()
    def openClientFile(self):
        progressDialog = QtGui.QProgressDialog()
        progressDialog.setAutoClose(False)
        progressDialog.setAutoReset(False)
        label = progressDialog.findChildren(QtGui.QLabel)[0]
        label.setFont(QtGui.QFont("Calibri", 12))
        button = progressDialog.findChildren(QtGui.QPushButton)[0]
        button.hide()
        progressBar = progressDialog.findChildren(QtGui.QProgressBar)[0]
        progressBar.hide()
        
    
        contract_selected = self.getSelectedContract()
        if contract_selected is not None:
            client_file = contract_selected.getAcheteur().sheet_path
            
            progressDialog.setWindowTitle(u"Ouverture en cours...")
            text = u"\n\nOuverture du fichier \n"+client_file[0]
            progressDialog.setLabelText(text)
            progressDialog.show()
            QtGui.QApplication.processEvents()
            
            self.openWorkSheet(client_file[0], client_file[1])
            
            progressDialog.close()
            QtGui.QApplication.processEvents()
            
        else:
            self.popupMessage("Fiche client inexistante...")
    
        
    @QtCore.Slot()
    def openFournisFile(self):
        progressDialog = QtGui.QProgressDialog()
        progressDialog.setAutoClose(False)
        progressDialog.setAutoReset(False)
        label = progressDialog.findChildren(QtGui.QLabel)[0]
        label.setFont(QtGui.QFont("Calibri", 12))
        button = progressDialog.findChildren(QtGui.QPushButton)[0]
        button.hide()
        progressBar = progressDialog.findChildren(QtGui.QProgressBar)[0]
        progressBar.hide()
        
        contract_selected = self.getSelectedContract()
        if contract_selected is not None:
            client_file = contract_selected.getVendeur().sheet_path
            
            progressDialog.setWindowTitle(u"Ouverture en cours...")
            text = u"\n\nOuverture du fichier \n"+client_file[0]
            progressDialog.setLabelText(text)
            progressDialog.show()
            QtGui.QApplication.processEvents()
            
            self.openWorkSheet(client_file[0], client_file[1])
            
            progressDialog.close()
            QtGui.QApplication.processEvents()
        else:
            self.popupMessage("Fiche fournisseur introuvable...")
            
    def openWorkSheet(self, workbook_path, worksheet_name):
        
        progressDialog = QtGui.QProgressDialog()
        progressDialog.setAutoClose(False)
        progressDialog.setAutoReset(False)
        label = progressDialog.findChildren(QtGui.QLabel)[0]
        label.setFont(QtGui.QFont("Calibri", 12))
        button = progressDialog.findChildren(QtGui.QPushButton)[0]
        button.hide()
        progressBar = progressDialog.findChildren(QtGui.QProgressBar)[0]
        progressBar.hide()
        
        if exists(workbook_path):
            
            progressDialog.setWindowTitle(u"Ouverture en cours...")
            text = u"\n\nOuverture du fichier \n"+workbook_path
            progressDialog.setLabelText(text)
            progressDialog.show()
            QtGui.QApplication.processEvents()
            
            xl = wc.Dispatch("Excel.Application")
            xl.Workbooks.Open(Filename=workbook_path, ReadOnly=1)
            xl.Worksheets(worksheet_name).Activate()
            xl.Visible = True
            del xl
            
            
            progressDialog.close()
            QtGui.QApplication.processEvents()
            
        else:
            self.popupMessage("Worksheet introuvable...")
    
    def addDelivery(self):
        dic = deliveryEditor.commandDelivery(self, self.getSelectedContract())
        if dic is not None: 
            ctr = self.getSelectedContract()
            ctr.newDelivery(dic)
            self.cDB.updateContract(ctr)
        
    def specifyResearch(self, sender):
        if "ctr" in sender.objectName():
            self.ui.rb_r_n_ctr.setChecked(True)
        elif "client" in sender.objectName():
            self.ui.rb_r_n_client.setChecked(True)
        elif "fourniss" in sender.objectName():
            self.ui.rb_r_n_fourniss.setChecked(True)
        self.ui.b_rechercher.setEnabled(True)
            
    def getSelectedContract(self):
        items_selected = self.t_ctr_list.selectedItems()
        if len(items_selected) < 1:
#            self.setButtonEnabled(False)
            return None
        return items_selected[0].ctr
        
    @QtCore.Slot()
    def setClientNumber(self):
        print "setClientNumber"
        contract_selected = self.getSelectedContract()
        if contract_selected is None:
            return 
        
        contract_selected.n_client = Question.askNumber(whatIsIt = "Numéro de contract client : ")
        self.cDB.updateContract(contract_selected)
        
    def setFournissNumber(self):
        print "setClientNumber"
        contract_selected = self.getSelectedContract()
        if contract_selected is None:
            return 
        
        contract_selected.n_fourniss = Question.askNumber(whatIsIt = "Numéro de contract fournisseur : ")
        self.cDB.updateContract(contract_selected)
        
    @QtCore.Slot()
    def newContract(self):
        contract_maker = ContractIniter(self)
#        contract_maker.resize(contract_maker.minimumSize())
        
        contract_maker.setAttribute(QtCore.Qt.WA_StyledBackground)
        contract_maker.show()
        
    @QtCore.Slot()
    def modifyContract(self):
        ctr = self.getSelectedContract()
        if ctr is None:
            return 
        
        editor = QtGui.QMainWindow(self)
        editor.setWindowTitle('Éditeur de contrat')
        contract_editor = ContractEditor()
        contract_editor.setCreatorMode(False)
        contract_editor.ui.label_13.hide()
        contract_editor.initEditor(ctr)
        editor.setCentralWidget(contract_editor)
#        QtCore.QObject.connect(contract_editor, QtCore.SIGNAL('s_close_widget'), editor.close)
        contract_editor.s_close_widget.connect(editor.close)
        
        editor.show()
    def closeEditor(self):
        print "received"        
        
    @QtCore.Slot()
    def printContract(self):
        self.printer.launch(self.getSelectedContract())
        
        
        
    @QtCore.Slot()
    def removeContract(self):
        ctr = self.getSelectedContract()
        if ctr is not None:
            message = "Êtes-vous sûr de vouloir supprimer définitivement le contrat n°"+str(ctr.n_contrat)+" ?"
            reply = QtGui.QMessageBox.question(self, 'Attention', message, QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
            if reply == QtGui.QMessageBox.Yes:
                threading.Thread(target=self.cDB.removeContract, args=(ctr,None,)).start()
#                self.cDB.removeContract(ctr)
        else:
            threading.Thread(target=self.cDB.removeContract, args=(ctr,None,)).start()
#            self.cDB.removeContract(ctr)
    
    @QtCore.Slot()
    def itemSelected(self):
        print "itemSelected"
        
    
    def updateOrdererYear(self):
        y_min, y_max = maxint, 0
        for ctr in self.cDB.getEveryContracts():
            if ctr is None:
                continue
            date = ctr.date_contrat
            year = int(date.split('/')[2])
            if year > y_max:
                y_max = year
            if year < y_min:
                y_min = year
                
        self.ui.cb_sort_year.blockSignals(True)
        self.ui.cb_sort_year.clear()
        self.ui.cb_sort_year.addItem("Année", userData = None)
        
        for y in range(y_min, y_max+1, 1):
            self.ui.cb_sort_year.addItem(str(y), userData = y)
        self.ui.cb_sort_year.blockSignals(False)
        
        index = self.ui.cb_sort_year.findText(str(datetime.datetime.now().year))
        if index < 0: index = 0
        self.ui.cb_sort_year.setCurrentIndex(index)
        
        
    def updateOrdererFourniss(self):
        self.ui.cb_sort_fourniss.blockSignals(True)
        self.ui.cb_sort_fourniss.clear()
        self.ui.cb_sort_fourniss.addItem("- Tous -", userData = None)
        
        client_list = self.oil_market.get_client(is_fournisseur=True)
        client_names = list(c.short_name.encode('utf-8') for c in client_list)
        
        zipped = zip(client_names, client_list)
        ordered_client_list = sorted(zipped, key = lambda client: client[0])
        for n, c in ordered_client_list:
            self.ui.cb_sort_fourniss.addItem(n, c)
            
            
        self.ui.cb_sort_fourniss.setCurrentIndex(0)
        self.ui.cb_sort_fourniss.blockSignals(False)
        
    def updateOrdererClient(self):
        self.ui.cb_sort_client_2.blockSignals(True)
        self.ui.cb_sort_client_2.clear()
        self.ui.cb_sort_client_2.addItem("- Tous -", userData = None)
        
        client_list = self.oil_market.get_client(is_fournisseur=False)
        client_names = list(c.short_name.encode('utf-8') for c in client_list)
        
        zipped = zip(client_names, client_list)
        ordered_client_list = sorted(zipped, key = lambda client: client[0])
        for n, c in ordered_client_list:
            self.ui.cb_sort_client_2.addItem(n, c)
            
        self.ui.cb_sort_client_2.setCurrentIndex(0)
        self.ui.cb_sort_client_2.blockSignals(False)
                
        
    def initOrdererMarchandise(self):
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
        
        
        
    def initCtrList(self):
        col1 = "Date".decode('utf-8').strip()
        col2 = "N°contrat".decode('utf-8').strip()
        col3 = "N°client".decode('utf-8').strip()
        col4 = "N°fournisseur".decode('utf-8').strip()
        col5 = "Client".decode('utf-8').strip()
        col6 = "Fournisseur".decode('utf-8').strip()
        col7 = "Marchandise".decode('utf-8').strip()
        col8 = "Courtage".decode('utf-8').strip()
        col9 = "Quantité (T)".decode('utf-8').strip()
        col10 = "Prix".decode('utf-8').strip()
        col11 = "Livraison".decode('utf-8').strip()
        col12 = "À livrer".decode('utf-8').strip()
        col13 = "À payer".decode('utf-8').strip()
        headers = [col1, col2, col3, col4, col5, col6, col7, col8, col9, col10, col11, col12, col13]
        
        self.t_ctr_list.setHeaderLabels(headers)
#        self.updateCtrList()
        self.t_ctr_list.setSortingEnabled(True)
#        self.t_ctr_list.header().setResizeMode(QtGui.QHeaderView.ResizeToContents)
        
#        self.t_ctr_list.header().setResizeMode(QtGui.QHeaderView.Interactive)
        
        font = self.t_ctr_list.header().font()
        font.setPointSize(10)
        self.t_ctr_list.header().setFont( font )
        for i in range(0, len(headers), 1):
            self.t_ctr_list.headerItem().setTextAlignment(i, QtCore.Qt.AlignCenter)
        
    def sortContractList(self, index = None):

        year = self.ui.cb_sort_year.itemData(self.ui.cb_sort_year.currentIndex())
        client = self.ui.cb_sort_client_2.itemData(self.ui.cb_sort_client_2.currentIndex())
        fourniss = self.ui.cb_sort_fourniss.itemData(self.ui.cb_sort_fourniss.currentIndex())
        if self.ui.cb_marchandise.currentIndex() <= 0:
            marchandise = None
        else:
            marchandise = self.ui.cb_marchandise.itemText(self.ui.cb_marchandise.currentIndex())
            marchandise = self.oil_market.get_code_from_name(marchandise)
            
        sorted_ctr_list = self.cDB.getContracts(by_year=year, by_client = client, by_fourniss=fourniss, by_marchandise=marchandise)

        return sorted_ctr_list 

    def updateCtrList(self, ctr_list = None):
        print "updateCtrList, arg : ", ctr_list
        
        self.t_ctr_list.clear()
        if ctr_list is None or isinstance(ctr_list, list) == False:
            ctr_list = self.sortContractList()
        
        itemlist = []
        for ctr in ctr_list:
            if ctr is None:
                itemlist = [' - ', ' - ', ' - ', ' - ', ' - ', ' - ', ' - ', ' - ', ' - ', ' - ', ' - ']
            else:
                full_marchandise = self.oil_market.getMarchandiseFullName(ctr.marchandise)
                monnaie = ' '+getFromConfig('monnaie', 'monnaies')[ctr.monnaie]['sym'].encode('utf8')
                if ctr.unite is not None:
                    unite = ' '+ctr.unite.title()
                else: unite = ""
        
                # TO BE DELETED
                acheteur = ctr.getAcheteur()
                if not hasattr(acheteur, "short_name"):
                    setattr(acheteur, 'short_name', self.oil_market.get_client(acheteur.nom, False).short_name)
                    self.cDB.updateContract(ctr)
                vendeur = ctr.getVendeur()
                if not hasattr(vendeur, "short_name"):
                    setattr(vendeur, 'short_name', self.oil_market.get_client(vendeur.nom, True).short_name)
                    self.cDB.updateContract(ctr)
                    
                nom_client = ctr.getClientName(shortest=True) + "\n" + ctr.get_uVilleAcheteur()
                nom_fourniss = ctr.getFournissName(shortest=True) + "\n" + ctr.get_uVilleVendeur()
                itemlist = [ctr.date_contrat, ctr.n_contrat, ctr.n_client, ctr.n_fourniss, nom_client, nom_fourniss, full_marchandise, ctr.courtage, format_num(ctr.qte_total)+unite, ctr.prix, "", format_num(ctr.reste_livraison)+unite, format_num(ctr.reste_paiement)+monnaie]
            newLine = TreeWidgetContract(self.t_ctr_list, ctr, itemlist)
            self.t_ctr_list.setItemWidget(newLine, 8, DeliveriesViewer(self, ctr))
            for i in range(0, 14, 1):
                newLine.setTextAlignment(i, QtCore.Qt.AlignCenter)
            
        self.t_ctr_list.header().setResizeMode(QtGui.QHeaderView.ResizeToContents)
        self.t_ctr_list.header().setResizeMode(QtGui.QHeaderView.Interactive)
        for i in range(0, len(itemlist), 1):
            self.t_ctr_list.resizeColumnToContents(i)
#        self.t_ctr_list.header().setResizeMode(self.t_ctr_list.columnCount()-3, QtGui.QHeaderView.Stretch)
        self.repaint()
    
        
    def setButtonEnabled(self, state):
        for i in range(self.ui.l_buttons.count()):
            b = self.ui.l_buttons.itemAt(i).widget()
            if isinstance(b, QtGui.QPushButton):
                b.setEnabled(state)
            
    @QtCore.Slot()
    def researchContract(self):
        if self.ui.rb_r_n_ctr.isChecked():
            num = str(self.ui.l_n_ctr.text())
            type_num = NUM_CTR
        elif self.ui.rb_r_n_client.isChecked():
            num = str(self.ui.l_n_client.text())
            type_num = NUM_CTR_C
        elif self.ui.rb_r_n_fourniss.isChecked():
            num = str(self.ui.l_n_fourniss.text())
            type_num = NUM_CTR_F
        if len(num)>0:
            ctr_found = self.cDB.getContractsByNum(num.rstrip(), type_num)
            self.updateCtrList(ctr_found)
        else:
            self.updateCtrList()
    
    @QtCore.Slot(str)
    def loadContractFromDeliveries(self, n_deliv):
        n_deliv = n_deliv.split('-')
        n_ctr = n_deliv[0]+'-'+n_deliv[1]
        ctr = self.cDB.getContractsByNum(n_ctr, NUM_CTR)[0]
        self.updateCtrList([ctr])
        
    def popupMessage(self, message, is_question = False):
        msgBox = QtGui.QMessageBox()
        msgBox.setText(message)
        msgBox.setWindowTitle('Problème')
        if is_question:
            msgBox.setWindowTitle('Question')
            msgBox.setStandardButtons(QtGui.QMessageBox.Ok | QtGui.QMessageBox.Cancel)
            msgBox.button(QtGui.QDialogButtonBox.Ok).setText("Valider")
            msgBox.button(QtGui.QDialogButtonBox.Cancel).setText("Annuler")
            msgBox.setDefaultButton(QtGui.QMessageBox.Ok)
        return msgBox.exec_()
        
    @QtCore.Slot()
    def showEvent(self, event):
#        self.updateCtrList()
        pass
    
    def FIAUpdated(self):
        for ctr in self.cDB.getEveryContracts():
            acheteur = ctr.getAcheteur()
            m_acheteur = self.oil_market.get_client(acheteur.nom, acheteur.type_client)
            if m_acheteur is not None:
                for k,v in m_acheteur.__dict__.items():
                    if not hasattr(acheteur, k) : 
                        setattr(acheteur, k, v)
                        self.cDB.updateContract(ctr)
        
        
#    def paintEvent(self, event):
#        opt = QtGui.QStyleOption()
#        opt.initFrom(self)
#        p = QtGui.QPainter(self)
#        self.style().drawPrimitive(QtGui.QStyle.PE_Widget, opt, p, self)
#        
    def main(self):
        self.show()
      
        
if __name__ == "__main__":
    import sys

    app = QtGui.QApplication(sys.argv)
    cc = ContractsManager()
    cc.main()
    sys.exit(app.exec_())
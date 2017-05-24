# -*- coding: utf-8 -*-
"""
Created on Thu Mar 30 16:40:03 2017

@author: Raph
"""

from PySide import QtCore, QtGui
import sys, os
import win32com.client as wc
from re import findall
import datetime


from ui_contracteditor import Ui_ContractEditor
from classes import ContractsDatabase, Market #,Contract
from utils import getFromConfig

QtCore.QTextCodec.setCodecForCStrings(QtCore.QTextCodec.codecForName('utf-8'))

class UsinesComboBox(QtGui.QComboBox):
    def __init__(self, parent = None):
        super(UsinesComboBox, self).__init__(parent)
        self.usineList = []
        
    def addItem(self, usine):
        super(UsinesComboBox, self).addItem(usine.getAdr())
        self.usineList.append(usine)
        
    def addItems(self, usine_list):
        super(UsinesComboBox, self).addItems([usine.getAdr() for usine in usine_list]) 
        self.usineList.append(usine)


class CalendarDeliveries(QtGui.QWidget):
    
    def __init__(self, parent = None):
        super(CalendarDeliveries, self).__init__(parent)
        
        self.setObjectName("calendar_dlv")
        
        mainLayout = QtGui.QVBoxLayout()
        self.month_names = ["Janvier", "Février", "Mars", "Avril", "Mai", "Juin", "Juillet", "Août", "Septembre", "Octobre", "Novembre", "Décembre"]
        self.month_values = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]
        
        self.last_year = datetime.datetime.now().year
        
        self.tab_w = QtGui.QTabWidget()
#        self.tab_w.tabsClosable(True)
        style = """
        QTabWidget::pane { \
              border-top: 2px solid #C2C7CB; \
              border-top: 2px solid #C2C7CB; \
          } \
        QTabWidget::tab { \
            border: 2px solid grey; \
            min-width: 8ex; \
            padding: 8px; \
        }
        """
#        self.tab_w.setStyleSheet(style)
        self.addNewTab(0)
        self.tab_w.addTab(QtGui.QWidget(), "+")
        
        mainLayout.addWidget(self.tab_w)
        self.setLayout(mainLayout)
        mainLayout.setSpacing(0)
        self.tab_w.setContentsMargins(0, 0, 0, 0)
        
        self.tab_w.currentChanged.connect(self.currentIndexChanged)
        
        
        w, h = self.tab_w.sizeHint().width(), self.tab_w.sizeHint().height()
        self.tab_w.setMaximumSize(w, h)
        self.tab_w.setMinimumSize(w, h)
        
    def loadCalendar(self, dlv_dic):
        ordered_years = sorted(dlv_dic.keys())
        for i in range(0, len(ordered_years), 1):
            newtab = self.createNewTab()
            childs = newtab.findChildren(QtGui.QTableWidget)
            table = childs[0]
            y = ordered_years[i]
            for j in range(0, len(self.month_values)):
                m = self.month_values[j]
                total = float(dlv_dic[y][m]["total"])
                item = table.item(0, j)
                
                if item is None: 
                    item = QtGui.QTableWidgetItem("")
                    item.setTextAlignment(QtCore.Qt.AlignCenter)
                    item.setData(QtCore.Qt.UserRole, str(int(m)-1))
                    item.setFlags(item.flags() | QtCore.Qt.ItemIsEditable)
                    item.setText(str(total))
                    table.setItem(0, j, item)
                else:
                    item.setText(str(total))
            self.addNewTab(tab = [newtab, y])
#        self.tab_w.removeTab(0)
        self.tab_w.widget(0).deleteLater()
        
    def currentIndexChanged(self, index):
        if index == self.tab_w.count()-1:
            self.addNewTab(index = None)
        
    def addNewTab(self, index = None, tab = None):
        self.blockSignals(True)
        if index is None and self.tab_w.count() > 0 : 
            index = self.tab_w.count()-1
        
        if tab is None:
            self.tab_w.insertTab(index, self.createNewTab(), str(self.last_year))
            self.last_year += 1
        else:
            self.last_year = int(tab[1])
            self.tab_w.insertTab(index, tab[0], str(self.last_year))
            self.last_year += 1
            
        self.tab_w.setCurrentIndex(self.tab_w.count()-2)
        self.blockSignals(False)
        

    def createNewTab(self):
        main = QtGui.QWidget()
        layout = QtGui.QHBoxLayout()
        tableWidget = QtGui.QTableWidget(1, 12)
        
        tableWidget.setHorizontalHeaderLabels(self.month_values)
        label = QtGui.QLabel("Mois", tableWidget)
        label.setAlignment(QtCore.Qt.AlignCenter)
        label.setAttribute(QtCore.Qt.WA_TransparentForMouseEvents)
        label.setGeometry(2, 1, tableWidget.verticalHeader().width()+65, tableWidget.horizontalHeader().height())
        tableWidget.setVerticalHeaderLabels(["Quantité"])
        
        tableWidget.horizontalHeader().setStretchLastSection(True)
        tableWidget.verticalHeader().setStretchLastSection(True)
        tableWidget.horizontalScrollBar().setDisabled(True)
        tableWidget.verticalScrollBar().setDisabled(True)
        
        month_id = 0
        for i in range(0, tableWidget.rowCount(), 1):
            for j in range(0, tableWidget.columnCount(), 1):
                item = QtGui.QTableWidgetItem()
                item.setTextAlignment(QtCore.Qt.AlignCenter)
                item.setData(QtCore.Qt.UserRole, str(month_id))
                item.setText("0")
                item.setFlags(item.flags() | QtCore.Qt.ItemIsEditable)
                tableWidget.setItem(i, j, item)
                month_id += 1
        
        tableWidget.resizeColumnsToContents()
        tableWidget.resizeRowsToContents()
        tableWidget.setFixedSize(tableWidget.horizontalHeader().length()+80, tableWidget.verticalHeader().length() + 35)

        layout.addWidget(tableWidget)
        main.setLayout(layout)
        
        return main
    
    def getSelection(self):
        # res[year][month] = {"total": ?, "done": ?}
        planning = {}
        total_planned = 0
        for t in range(0, self.tab_w.count()-1):
            year =  self.tab_w.tabText(t)
            tab = self.tab_w.widget(t)
            table = tab.findChildren(QtGui.QTableWidget)[0]
            months = {}
            n_column = table.columnCount()
            tmp_total = 0
            for c in range(0, n_column, 1):
                cell = table.item(0, c)
                qte = cell.text()
                state = {"total": qte, "done": 0}
                months[self.month_values[c]] = state
                tmp_total += float(qte)
            if tmp_total > 0:
                planning[year] = months
            total_planned += tmp_total
        return total_planned, planning
            





class ContractEditor(QtGui.QWidget, QtCore.QObject):

    s_usine_selected = QtCore.Signal()
    enter_key_pressed = QtCore.Signal()
    s_contract_edited = QtCore.Signal()
    s_contract_validated = QtCore.Signal()
    s_close_widget = QtCore.Signal()
        
    def __init__(self, parent=None):
        super(ContractEditor, self).__init__(parent)
        self.ui = Ui_ContractEditor()
        self.ui.setupUi(self)
        self.setCreatorMode() # precis if we modify an existant contract or not
        
        self.cDB = ContractsDatabase()
        self.oil_market = Market()
#        self.comm = self.cDB.communicator
#        self.comm.s_cDB_updated.connect(self.updateCtrList)
#        self.new_contract = Contract()
        self.new_contract = None
        

        self.w_dlv_date = CalendarDeliveries()
        layout = QtGui.QVBoxLayout()
        layout.addWidget(self.w_dlv_date)
        self.ui.date_livraison.setLayout(layout)
        
        self.ui.date_livraison.updateGeometry()
        self.ui.date_livraison.resize(self.w_dlv_date.minimumSize())
        self.w_dlv_date.updateGeometry()
        self.w_dlv_date.resize(self.w_dlv_date.minimumSize())
        
        self.ui.date_livraison.adjustSize()
        
        self.ui.n_contrat.setEnabled(True)
        self.connectionsManager()
        
        self.initMonnaie()
        self.initMarchandiseList()
        self.initPaiementList()
        self.initLogementList()
        
        
    def setCreatorMode(self, b = True):
        self.creator_mode = b
    
    
    def connectionsManager(self):
        self.ui.cb_marchandise.currentIndexChanged[int].connect(self.currentMarchandiseChanged)
#        self.ui.cb_nom_acheteur.editTextChanged[str].connect(self.updateClientList)
#        self.ui.cb_nom_vendeur.editTextChanged[str].connect(self.updateClientList)
        #lorsque un nom de client est selectionné dans la liste
        self.ui.cb_nom_acheteur.currentIndexChanged[int].connect(self.updateAdressList)
        self.ui.cb_nom_vendeur.currentIndexChanged[int].connect(self.updateAdressList)
        
        self.ui.quantite.textEdited[str].connect(self.updateUnite)
        
        self.ui.b_valid.clicked.connect(self.validateContract)
        self.ui.b_cancel.clicked.connect(self.close)
        self.ui.b_fiche_acheteur.clicked.connect(self.openClientFile)
        self.ui.b_fiche_vendeur.clicked.connect(self.openFournissFile)
        
        
        
    def initEditor(self, ctr = None):
        print "initEditor"
        if ctr is None: 
            self.new_contract = self.cDB.newContract()
        else:
            self.new_contract = ctr
        
        self.ui.n_contrat.setText(self.new_contract.n_contrat)
        
        self.initClientList()
        
        if self.new_contract.marchandise is not None:
            if not isinstance(self.new_contract.marchandise, int):
                tmp_marchandise = self.oil_market.getMarchandiseFullName(self.new_contract.marchandise)
                self.ui.cb_marchandise.setCurrentIndex(self.ui.cb_marchandise.findText(tmp_marchandise))
            else:
                self.ui.cb_marchandise.setCurrentIndex(self.new_contract.marchandise)
            
        # INITIALIZATION OF FOURNISSEUR NAME AND FOUNISSEUR ADR IF EXIST
        if self.new_contract.usine_depart is not None: #usine vendeur
            index = 0
            while self.new_contract.usine_depart.proprietaire.nom not in self.ui.cb_nom_vendeur.itemText(index).encode('utf-8'):
                index += 1
                if index > self.ui.cb_nom_vendeur.count():
                    index = -1
                    break
            self.ui.cb_nom_vendeur.setCurrentIndex(index)
            self.updateAdressList(emitter=self.ui.cb_nom_vendeur)
            
            index = 0
            while self.new_contract.usine_depart.getAdr() != self.ui.cb_adr_depart.itemText(index):
                index += 1
                if index > self.ui.cb_adr_depart.count():
                    index = -1
                    break
            self.ui.cb_adr_depart.setCurrentIndex(index)
            
            
        # INITIALIZATION OF CLIENT NAME AND CLIENT ADR IF EXIST
        if self.new_contract.usine_destination is not None:
            index = 0
            while self.new_contract.usine_destination.proprietaire.nom not in self.ui.cb_nom_acheteur.itemText(index):
                index += 1
                if index > self.ui.cb_nom_acheteur.count():
                    index = -1
                    break
            self.ui.cb_nom_acheteur.setCurrentIndex(index)
            self.updateAdressList(emitter=self.ui.cb_nom_acheteur)
            
            index = 0
            while self.new_contract.usine_destination.getAdr() != self.ui.cb_adr_livraison.itemText(index):
                index += 1
                if index > self.ui.cb_adr_livraison.count():
                    index = -1
                    break
            self.ui.cb_adr_livraison.setCurrentIndex(index)
            
        
        # INITIALIZATION OF CONTRACT DATE IF EXIST
        if self.new_contract.date_contrat is not None:
            self.ui.date_ctr.setDate(QtCore.QDate.fromString(self.new_contract.date_contrat, "dd/MM/yyyy"))
        else:
            self.ui.date_ctr.setDate(QtCore.QDate.currentDate())
            
        # INITIALIZATION OF CTR MONNEY
        if self.new_contract.monnaie is not None:
            for i in range(0, self.ui.cb_monnaie.count()):
                if self.ui.cb_monnaie.itemData(i) == self.new_contract.monnaie:
                    self.ui.cb_monnaie.setCurrentIndex(i)
                    break
                
        # INITIALIZATION OF CTR UNIT
        if self.new_contract.unite is not None:
            for i in range(0, self.ui.cb_unite.count()):
                if self.ui.cb_unite.itemData(i) == self.new_contract.unite:
                    self.ui.cb_unite.setCurrentIndex(i)
                    break
                
        if self.new_contract.prix is not None:
            self.ui.prix.setText(self.new_contract.prix)
        if self.new_contract.courtage is not None:
            self.ui.courtage.setText(self.new_contract.courtage)
        if self.new_contract.is_franco is True:
            self.ui.cb_franco.setChecked(True)
        if self.new_contract.ville is not None and len(self.new_contract.ville)>0:
            self.ui.l_ville.setText(self.new_contract.ville)
        if self.new_contract.logement is not None:
            self.ui.cb_logement.setCurrentIndex(self.ui.cb_logement.findText(self.new_contract.logement))
        if self.new_contract.periode_livraison is not None:
            self.w_dlv_date.loadCalendar(self.new_contract.periode_livraison)
        if self.new_contract.quantite is not None:
            self.ui.quantite.setText(self.new_contract.quantite)
        if self.new_contract.qte_total is not None:
            self.ui.qte_total.setText(str(self.new_contract.qte_total))
        if self.new_contract.paiement is not None:
            self.ui.cb_paiement.setCurrentIndex(self.ui.cb_paiement.findText(self.new_contract.paiement))
        
        
    def initMonnaie(self):
        print "initMonnaie"
        monnaies = getFromConfig('monnaie', 'monnaies')
        sorted_monnaies = sorted(monnaies, key = lambda m: m['code'])
        for m in sorted_monnaies:
            self.ui.cb_monnaie.addItem(m['sym'].encode('utf8'), userData=m['code'])
        self.ui.cb_monnaie.setCurrentIndex(0)
        
        unites = getFromConfig('unite', 'unites')
        for u in unites:
            self.ui.cb_unite.addItem(u['sym'].encode('utf8').title(), userData=u['sym'].lower())
        self.ui.cb_unite.setCurrentIndex(0)
        
    def initMarchandiseList(self):
        print "initMarchandiseList"
        marchandise_list = self.oil_market.marchandises_list['fr']
        ordered_marchandise_list = sorted(marchandise_list)
        self.updateComboBox(self.ui.cb_marchandise, ordered_marchandise_list)
        completer = QtGui.QCompleter(marchandise_list)
        completer.setCaseSensitivity(QtCore.Qt.CaseInsensitive)
        completer.setCompletionMode(QtGui.QCompleter.UnfilteredPopupCompletion)
        self.ui.cb_marchandise.setCompleter(completer)
        
#    def updateMarchandiseList(self, current_list = None):
#        print "updateMarchandiseList"
#        if current_list is None:
#            marchandise_list = self.oil_market.marchandises_list['fr']
#        else:
#            marchandise_list = current_list
#        marchandise_list = sorted(marchandise_list)
#        if self.ui.cb_adr_depart.currentIndex() >= 0 or self.ui.cb_adr_livraison.currentIndex() >= 0:
#            if self.ui.cb_adr_livraison.currentIndex() >= 0:
#                from Classes import Usine
#                usine = self.ui.cb_adr_depart.itemData(i)
#                for marchandise in usine.produits:
#                    if 
    
    def initPaiementList(self):
        print "initPaiementList"
        paiement_list = self.oil_market.paiements['fr']
        ordered_paiement_list = sorted(paiement_list)
        self.updateComboBox(self.ui.cb_paiement, ordered_paiement_list)
        
        
    def initLogementList(self):
        print "initMarchandiseList"
        logement_list = self.oil_market.logements['fr']
        ordered_logement_list = sorted(logement_list)
        self.updateComboBox(self.ui.cb_logement, ordered_logement_list)
        
    @QtCore.Slot(str)
    def initClientList(self, marchandise_name = ""):
        # called when marchandise is edited
        print "initClientList"
        if len(marchandise_name) > 0:
            usine_acheteur_possibles = self.oil_market.get_clients_from_marchandise(marchandise_name, is_fournisseur=False)
            client_list = list(set([ u.proprietaire.nom for u in usine_acheteur_possibles ]))
        else:
            client_list = list(set([ c.nom for c in self.oil_market.get_client(is_fournisseur=False) ]))
#        print "acheteur_list \n ", client_list
        client_list = sorted(client_list)
        self.updateComboBox(self.ui.cb_nom_acheteur, client_list)
        completer = QtGui.QCompleter(client_list)
        completer.setCaseSensitivity(QtCore.Qt.CaseInsensitive)
        completer.setCompletionMode(QtGui.QCompleter.InlineCompletion)
        self.ui.cb_nom_acheteur.setCompleter(completer)
        
        if len(marchandise_name)>0:
            usine_vendeur_possibles = self.oil_market.get_clients_from_marchandise(marchandise_name, is_fournisseur=True)
            client_list = list(set([ u.proprietaire.nom for u in usine_vendeur_possibles ]))
        else:
            client_list = list(set([ c.nom for c in self.oil_market.get_client(is_fournisseur=True) ]))
#        print "vendeur_list \n ", client_list
        client_list = sorted(client_list)
        self.updateComboBox(self.ui.cb_nom_vendeur, client_list)
        completer = QtGui.QCompleter(client_list)
        completer.setCaseSensitivity(QtCore.Qt.CaseInsensitive)
        completer.setCompletionMode(QtGui.QCompleter.InlineCompletion)
        self.ui.cb_nom_vendeur.setCompleter(completer)


    def updateComboBox(self, cb, items = None, blockSignals = True, text = ""):
        print "updateComboBox ", cb.objectName()
        cb.blockSignals(blockSignals)
        cb.clear()
        if items is not None:
            cb.addItems(items)
        cb.setCurrentIndex(-1)
        cb.setEditText(text)
        cb.blockSignals(False)
            
    @QtCore.Slot(str)
    def updateTotalQte(self, text):
        matches = findall(r"[-+]?\d*\.*\d+", text)
        if len(matches) > 0:
            qte = matches[-1]
#            print qte
            self.ui.qte_total.setText(qte)
    
    @QtCore.Slot(str)    
    def updateUnite(self, text):
        if 'kilo' in text or 'kg' in text:
            self.ui.cb_unite.setCurrentIndex(self.ui.cb_unite.findData('kg'))
        else:
            self.ui.cb_unite.setCurrentIndex(self.ui.cb_unite.findData('t'))
            
            
#    @QtCore.Slot(str)    
#    def updateMarchandise(self, text):
#        # recupere l'emetteur et nettoie le combobox en question
#        sender = self.sender()
#        print self.ui.cb_marchandise.currentIndex()
#        print "updateMarchandise; signal from ", sender.objectName()
#        text = _format(text, True, True)
#        potentials = self.oil_market.getNearestMarchandise(text)
#        ordered_marchandise_list = sorted(potentials)
#        self.updateComboBox(sender, ordered_marchandise_list, text=text)     
            
    @QtCore.Slot(int)
    def currentMarchandiseChanged(self, index):
        print "currentMarchandiseChanged ", index
        sender = self.sender()
        self.new_contract.marchandise = self.oil_market.get_code_from_name(sender.itemText(index))

    @QtCore.Slot(str)
    def updateClientList(self, text, cb_widget = None):
        # recupere l'emetteur et nettoie le combobox en question
        # puis met à jour la liste des noms similaires
        cb_client = cb_widget or self.sender()
        print "updateClientList; signal from ", cb_client.objectName()
        
        clients = []
        if cb_client.objectName() == "cb_nom_vendeur" or cb_client.objectName() == "cb_nom_acheteur" :
            clients = self.oil_market.getNearestClient(text.encode('utf8'), 'vendeur' in cb_client.objectName())
        elif len(self.ui.cb_marchandise.currentText()) > 0:
            clients = [ u.proprietaire.nom for u in self.oil_market.get_clients_from_marchandise(self.ui.cb_marchandise.currentText(), 'vendeur' in cb_client.objectName())]
        else:
            clients = [ u.proprietaire.nom for u in self.oil_market.get_client(is_fournisseur = 'vendeur' in cb_client.objectName())]
        
        ordered_clients_list = sorted(clients)
        if len(ordered_clients_list) == 0:
            print("Probable error when updateClientList")
            
        self.updateComboBox(cb_client, ordered_clients_list, text=text)
        
        
    @QtCore.Slot(int)
    def updateAdressList(self, client_index = None, emitter = None):
        #recupere l'emetteur et la destination
        if emitter is None:
            cb_client = self.sender()
        else:
            cb_client = emitter
        print "updateAdressList; signal from ", cb_client.objectName(), client_index
        
        if 'vendeur' in cb_client.objectName():
            cb_adr = self.ui.cb_adr_depart
        else:
            cb_adr = self.ui.cb_adr_livraison
            
        cb_adr.blockSignals(True)
        # et met a jour la liste des adresses disponibles
        while cb_adr.count() > 0:
            cb_adr.removeItem(0)
            
    
        # si la marchandise est bien renseignée, on ne met que les usines correspondantes. Sinon on les met toutes.
#        if len(self.ui.cb_marchandise.text()) > 0:
#            for usine in self.oil_market.get_clients_from_marchandise(self.ui.cb_marchandise.text(), 'vendeur' in cb_client.objectName()):
#                if usine.proprietaire.nom == cb_client.currentText().encode('utf-8'):
#                    cb_adr.addItem(getInlineArray(usine.adresse), userData = usine)
##                    cb_adr.setCurrentIndex(0)
#        else:
        for usine in self.oil_market.get_client(cb_client.currentText(), 'vendeur' in cb_client.objectName()).usines:
            adr = usine.getAdr()
            cb_adr.addItem(adr, userData = usine)
            
        
#        cb_adr.setCurrentIndex(0)
        cb_adr.blockSignals(False)
        cb_adr.setCurrentIndex(-1)
        
        
    @QtCore.Slot(int)
    def updateAdrCtr(self, index):
        sender = self.sender()
        print "updateAdrCtr; signal from ", sender.objectName(), index
#        
#        if "depart" in sender.objectName():
#            self.new_contract.usine_depart = self.ui.cb_adr_depart.itemData(index)
#        elif "livraison" in sender.objectName():
#            self.new_contract.usine_destination = self.ui.cb_adr_livraison.itemData(index)

        
    @QtCore.Slot()
    def validateContract(self):
        
        self.new_contract.n_contrat = self.ui.n_contrat.text()
        
        i = self.ui.cb_adr_depart.currentIndex()
        data = self.ui.cb_adr_depart.itemData( i )
        self.new_contract.usine_depart = data
        
        i = self.ui.cb_adr_livraison.currentIndex()
        data = self.ui.cb_adr_livraison.itemData( i )
        self.new_contract.usine_destination = data
            
        self.new_contract.date_contrat = str(self.ui.date_ctr.date().toString("dd/MM/yyyy"))
        self.new_contract.is_franco = self.ui.cb_franco.isChecked()
        self.new_contract.ville = self.ui.l_ville.text()
        
        tmp = findall(r"[-+]?\d*\.*\d+", self.ui.qte_total.text())
        if len(tmp) > 0:
            self.new_contract.qte_total = float(tmp[0])
        else:
            self.new_contract.qte_total = 0.0
            
        self.new_contract.periode_livraison = self.w_dlv_date.getSelection()[1]
        self.new_contract.prix = self.ui.prix.text().encode('utf8')
        self.new_contract.courtage = self.ui.courtage.text().encode('utf8')
        self.new_contract.paiement = self.ui.cb_paiement.currentText()
        self.new_contract.logement = self.ui.cb_logement.currentText()
        self.new_contract.quantite = self.ui.quantite.text()
        
        self.new_contract.monnaie = self.ui.cb_monnaie.itemData(self.ui.cb_monnaie.currentIndex())
        self.new_contract.unite = self.ui.cb_unite.itemData(self.ui.cb_unite.currentIndex())
        
#        self.new_contract.marchandise = self.ui.cb_marchandise.findText(self.ui.cb_marchandise.currentText())
        print self.new_contract.marchandise
        if self.checkFormular() is False:
            return
        
        self.cDB.updateContract(self.new_contract)
        self.new_contract  = None
        print "Validated; ctr is now ", self.new_contract
#        self.s_contract_validated.emit()
        
#        if self.creator_mode is False:
        self.close()
            
    def checkFormular(self):
        
        to_complete = 0
#        
        if self.ui.cb_nom_acheteur.currentIndex() < 0:
            to_complete += 1
            self.ui.cb_nom_acheteur.setStyleSheet("#cb_nom_acheteur { border: 3px solid red; }")
        else:
            self.ui.cb_nom_acheteur.setStyleSheet("")
            
        if self.ui.cb_nom_vendeur.currentIndex() < 0:
            to_complete += 1
            self.ui.cb_nom_vendeur.setStyleSheet("#cb_nom_vendeur { border: 3px solid red; }")
        else:
            self.ui.cb_nom_vendeur.setStyleSheet("")
        
        
        if self.ui.cb_adr_depart.currentIndex() < 0:
            to_complete += 1
            self.ui.cb_adr_depart.setStyleSheet("#cb_adr_depart { border: 3px solid red; }")
        else:
            self.ui.cb_adr_depart.setStyleSheet("")
            
        if self.ui.cb_adr_livraison.currentIndex() < 0:
            to_complete += 1
            self.ui.cb_adr_livraison.setStyleSheet("#cb_adr_livraison { border: 3px solid red; }")
        else:
            self.ui.cb_adr_livraison.setStyleSheet("")
        
        if self.new_contract.marchandise is None or len(self.new_contract.marchandise) < 0 or self.oil_market.marchandiseExist(self.new_contract.marchandise) is False:
            to_complete += 1
            self.ui.cb_marchandise.setStyleSheet("#cb_marchandise { border: 3px solid red; }")
        else:
            self.ui.cb_marchandise.setStyleSheet("")
        
        if self.new_contract.qte_total <= 0:
            to_complete += 1
            self.ui.qte_total.setStyleSheet("#qte_total { border: 3px solid red; }")
        else: 
            self.ui.qte_total.setStyleSheet("")
#            total = self.w_dlv_date.getSelection()[0]
#            if total == 0.0:
#                to_complete += 1
#                self.ui.date_livraison.setStyleSheet("#date_livraison { border: 3px solid red; }")
#            elif total > self.new_contract.qte_total:
#                to_complete += 1
#                self.ui.date_livraison.setStyleSheet("#date_livraison { border: 3px solid red; }")
#            else: 
#                self.ui.date_livraison.setStyleSheet("")
                
        if to_complete > 0:
            return False
        return True
    
        
        
            
            
            
    @QtCore.Slot(str)
    def saveLink(self, ctr_link):
        pass
#        self.new_contract.pdf_link = ctr_link
#        if self.creator_mode is True:
#            self.cDB.updateContract(self.new_contract)
##            self.resetPage()
#        else:
#            self.cDB.updateContract(self.new_contract)
#            self.parent().close()
#            self.s_contract_edited.emit()


    @QtCore.Slot()
    def resetPage(self):
        print "resetPage"
        self.blockSignals(True)
            
        items = (self.ui.formLayout.itemAt(i, QtGui.QFormLayout.FieldRole) for i in range(self.ui.formLayout.rowCount()) if self.ui.formLayout.itemAt(i, QtGui.QFormLayout.FieldRole) is not None) 
        for child in items:
            child = child.widget()
            if isinstance(child, QtGui.QLineEdit) or isinstance(child, QtGui.QPlainTextEdit) or isinstance(child, QtGui.QTextEdit):
                child.clear()
            elif isinstance(child, QtGui.QComboBox):
                self.updateComboBox(child)
        self.blockSignals(False)        


    @QtCore.Slot()
    def cancelContract(self):
        if self.creator_mode == True:
            message = "Êtes-vous sûr de vouloir annuler le contrat en cours ?"
            reply = QtGui.QMessageBox.question(self, 'Attention', message, QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
            
            if reply == QtGui.QMessageBox.Yes:
                self.cDB.cancelContract(self.new_contract)
                self.new_contract = None
                self.parent().parent().setCurrentIndex(0)
        else:
            message = "Annuler les modifications ?"
            reply = QtGui.QMessageBox.question(self, 'Attention', message, QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
            if reply == QtGui.QMessageBox.Yes:
                self.hide()
                self.closeWindow()
    
    
    def popupReinitialisation(self):
        msgBox = QtGui.QMessageBox()
        msgBox.setText("Avant de continuer : ")
        msgBox.setInformativeText("Souhaitez-vous initier un nouveau contrat ? ou modifier le courant ?")
        b_nouveau_ctr = msgBox.addButton(self.tr("Nouveau"), QtGui.QMessageBox.ActionRole)
        abortButton = msgBox.addButton(QtGui.QMessageBox.Abort)
        b_reinit_ctr = msgBox.addButton(self.tr("Réinitialiser"), QtGui.QMessageBox.ActionRole)
        
        msgBox.setDefaultButton(b_nouveau_ctr)
        
        msgBox.exec_()
        if msgBox.clickedButton() == abortButton:
            return 0
        elif msgBox.clickedButton() == b_reinit_ctr:
            return 1
        elif msgBox.clickedButton() == b_nouveau_ctr:
            return 2
    
    @QtCore.Slot()
    def openClientFile(self):
        client = self.oil_market.get_client(self.ui.cb_nom_acheteur.currentText(), is_fournisseur=False)

        if client is None:
            return
        
        client_file = client.sheet_path
        try:
            self.openWorkSheet(client_file[0], client_file[1])
        except:
            self.popupMessage("Fiche client introuvable...")
            
    
        
    @QtCore.Slot()
    def openFournissFile(self):
        fourniss = self.oil_market.get_client(self.ui.cb_nom_vendeur.currentText(), is_fournisseur=True)

        if fourniss is None:
            return
        
        fourniss_file = fourniss.sheet_path
        try:
            self.openWorkSheet(fourniss_file[0], fourniss_file[1])
        except:
            self.popupMessage("Fiche fournisseur introuvable...")
            
    
    def openWorkSheet(self, workbook_path, worksheet_name):
        if os.path.exists(workbook_path):
            xl = wc.Dispatch("Excel.Application")
            xl.Workbooks.Open(Filename=workbook_path, ReadOnly=1)
            xl.Worksheets(worksheet_name).Activate()
            xl.Visible = True
            del xl
        else:
            self.popupMessage("Worksheet introuvable...")
            
            
    def closeWindow(self):
        parent = self.parent()
        parent.close()
#        self.close
        
        
    def closeEvent(self, event):
        if self.creator_mode is False:
            message = "Annuler les modifications ?"
            reply = QtGui.QMessageBox.question(self, 'Attention', message, QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
            if reply == QtGui.QMessageBox.Yes:
                self.new_contract = None
                self.s_close_widget.emit()
                event.ignore()
            else:
                event.ignore()
        else:
            if self.parent().isVisible():
                self.s_close_widget.emit()
            event.accept()
                
          
#    def showEvent(self, event):
#        if self.new_contract is None:
#            self.initEditor()

    def keyPressEvent(self, e):
        if e.key() == QtCore.Qt.Key_Return or e.key() == QtCore.Qt.Key_Enter:
            self.validateContract()
    
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
        
    def main(self):
        self.show()
#        self.showFullScreen()
#        self.showMaximized()
    
if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    myCE = ContractEditor()
    myCE.main()
    sys.exit(app.exec_())
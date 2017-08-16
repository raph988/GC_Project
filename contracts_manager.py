# -*- coding: utf-8 -*-
"""
Created on Thu Mar 30 08:46:55 2017

@author: Raph
"""


from PySide import QtCore, QtGui
from sys import maxint
import datetime, inspect
from PIL import ImageFont

import win32com.client as wc
from os import listdir, startfile
from os.path import join, exists
import threading, re

from ui_contracts_manager import Ui_modif_contract as Ui_ContractsManager
from delivery_manager import deliveryEditor
from contract_initer import ContractIniter
from contract_editor import ContractEditor
from pdf_creator import PDFCreator

from utils import getFromConfig
#from utils import mathTex_to_QPixmap, format_num, TexPixmap
from utils import format_num, TexPixmap

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
        self.setAcceptDrops(True)
        self.setDragEnabled(True)
        self.setDragDropMode(QtGui.QAbstractItemView.DragDrop)
        self.setDefaultDropAction(QtCore.Qt.CopyAction)
        
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
            
            html = "<table>"
            for ctr in self.selectedItems():
                html += "<tr>"
                for i in range( 0, ctr.columnCount(), 1):
                    text = ctr.text(i)
                    if i != 6:
                        text = text.replace('\n','<br/>')
                    html += "<td>"+text+"</td>"
                html += "</tr>"
            html += "</table>"
            event.mimeData().setHtml(html)
                
            event.ignore()
            
    def dropEvent(self, event):
        
        print "ctr drop event"
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


class TreeWidgetItemLabel(QtGui.QWidget):
    def __init__(self, parent=None, text=""):
        super(TreeWidgetItemLabel, self).__init__(parent)
        mainLayout = QtGui.QVBoxLayout()
        self.myLabel = QtGui.QLabel()
        self.myLabel.setText("<span>"+text+"</span>")
        self.myLabel.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignCenter)
        mainLayout.addWidget(self.myLabel)
        self.setLayout(mainLayout)
        self.setAttribute(QtCore.Qt.WA_TransparentForMouseEvents)


from matplotlib.figure import Figure
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas

class MathTextLabel(QtGui.QWidget):
    def __init__(self, mathText, size, parent=None,):
        QtGui.QWidget.__init__(self, parent)
 
        l=QtGui.QVBoxLayout(self)
        l.setContentsMargins(0,0,0,0)
 
        r,g,b,a=self.palette().base().color().getRgbF()
 
        self._figure=Figure(edgecolor=(r,g,b), facecolor=(r,g,b))
        self._canvas=FigureCanvas(self._figure)
        l.addWidget(self._canvas)
 
        self._figure.clear()
        text=self._figure.suptitle(
            mathText,
            x=0.0,
            y=1.0,
            horizontalalignment='left',
            verticalalignment='top',
            size = size)
#            size=qApp.font().pointSize()*2)
        self._canvas.draw()
 
        (x0,y0),(x1,y1) = text.get_window_extent().get_points()
        w= x1-x0; h=y1-y0
 
        self._figure.set_size_inches(w/80, h/80)
        self.setFixedSize(w,h)

class DeliveriesViewer(QtGui.QWidget):
    
    def __init__(self, parent=None, ctr=None):
        super(DeliveriesViewer, self).__init__(parent)
        if ctr is None: return
        
        self.setObjectName("calendar_dlv")
        self.month_values = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]
        dlv_list = ctr.periode_livraison
        self.QPixTex = TexPixmap()
        
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
                    s = str(delivered)
                    p_size = 12
                else:
                    q = '$\\frac{'+delivered+'}{'+total+'}$'
                    s = str(delivered) + "/"+ str(total)
                    p_size = 14
#                pixmap = mathTex_to_QPixmap(q, p_size)
#                pixmap= self.QPixTex.mathTex_to_QPixmap(q, p_size)
#                pixmap = MathTextLabel(q, p_size)
                
                widget = QtGui.QWidget()
#                label = QtGui.QLabel(s)
#                widget = MathTextLabel(q, p_size)
                layout = QtGui.QHBoxLayout()
                label = QtGui.QLabel(s)
                label.setFont(QtGui.QFont("Calibri", 12))
                label.setMaximumSize(QtCore.QSize(100, 32))
                label.setScaledContents(True)
#                label.setPixmap(pixmap)
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
#        for i in range(0, len(itemlist), 1):
                self.tableWidget.resizeColumnToContents(j)
                
#        self.tableWidget.resizeRowsToContents()
#        self.tableWidget.resizeColumnsToContents()
        
        
#from PySide import QtUiTools

class ContractsManager(QtGui.QMainWindow, QtCore.QObject):
    
    s_addDelivery = QtCore.Signal(object)
    
    def __init__(self, parent = None):
        super(ContractsManager, self).__init__(parent)
        self.ui = Ui_ContractsManager()
        self.ui.setupUi(self)
        
#        self.widget = QtUiTools.QUiLoader().load("../interface_GC/accueil.ui")
#        self.ui = self.widget()
        
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
        self.ui.t_ctr_total.setIndentation(0)
        self.initOrdererMarchandise()
        
        self.ui.cb_marchandise.view().setAlternatingRowColors(True)
        self.ui.cb_sort_client_2.view().setAlternatingRowColors(True)
        self.ui.cb_sort_fourniss.view().setAlternatingRowColors(True)
        
        
        self.printer = PDFCreator(self)
        self.printer.setAttribute(QtCore.Qt.WA_StyledBackground)
        
        
        self.popMenu = QtGui.QMenu(self)
        self.actionPDF = QtGui.QAction("Voir le contrat PDF", self)
        self.actionPDF.triggered.connect(self.openPdfContract)
        self.actionAddNumberC = QtGui.QAction("Ajouter numero client", self)
        self.actionAddNumberC.triggered.connect(self.setClientNumber)
        self.actionAddNumberF = QtGui.QAction("Ajouter numero fournisseur", self)
        self.actionAddNumberF.triggered.connect(self.setFournissNumber)
        self.actionAddDelivery = QtGui.QAction("Nouvelle livraison", self)
        self.actionAddDelivery.triggered.connect(self.addDelivery)
        self.actionRemoveCtr = QtGui.QAction("Supprimer le contrat", self)
        self.actionRemoveCtr.triggered.connect(self.removeContract)
        self.actionModifyCtr = QtGui.QAction("Voir/modifier le contrat", self)
        self.actionModifyCtr.triggered.connect(self.modifyContract)
        self.actionAccessToClient = QtGui.QAction("Fiche client", self)
        self.actionAccessToClient.triggered.connect(self.openClientFile)
        self.actionAccessToFournis = QtGui.QAction("Fiche fournisseur", self)
        self.actionAccessToFournis.triggered.connect(self.openFournisFile)
        self.actionPrint = QtGui.QAction("Créer le contrat PDF", self)
        self.actionPrint.triggered.connect(self.printContract)
        self.actionNotes = QtGui.QAction("Notes du contrat", self)
        self.actionNotes.triggered.connect(self.showCtrNotes)
        
        self.popMenu.addAction(self.actionAddDelivery)
        self.popMenu.addSeparator()
        self.popMenu.addAction(self.actionPDF)
        self.popMenu.addAction(self.actionPrint)
        self.popMenu.addAction(self.actionModifyCtr)
        self.popMenu.addAction(self.actionNotes)
        self.popMenu.addSeparator()
        self.popMenu.addAction(self.actionAccessToClient)
        self.popMenu.addAction(self.actionAccessToFournis)
        self.popMenu.addSeparator()
        self.popMenu.addAction(self.actionAddNumberC)
        self.popMenu.addAction(self.actionAddNumberF)
        self.popMenu.addSeparator()
        self.popMenu.addAction(self.actionRemoveCtr)
        
        
        self.initCtrList()
        self.initOrdererClient()
        self.initOrdererFourniss()
        self.updateOrdererYear()
        
        self.ui.cb_marchandise.currentIndexChanged.connect(self.updateCtrList)
        self.ui.cb_sort_year.currentIndexChanged.connect(self.updateCtrList)
        self.ui.cb_sort_client_2.currentIndexChanged.connect(self.updateCtrList)
        self.ui.cb_sort_fourniss.currentIndexChanged.connect(self.updateCtrList)
        
#        self.comm.s_cDB_updated.connect(self.updateCtrList)
        self.comm.s_cDB_updated.connect(self.updateOrdererYear)
        self.ui.b_reinit_list.clicked.connect(self.reinitSorters)
        
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
        try:
            if event.type() == QtCore.QEvent.MouseButtonRelease:
                if obj == self.ui.l_n_client or obj == self.ui.l_n_ctr or obj == self.ui.l_n_fourniss:
                    self.specifyResearch(obj)
                    return True
        except:pass
        return False
    

    def customContextMenu(self, pos):
        if self.getSelectedContract() is not None:
            self.popMenu.exec_(self.t_ctr_list.mapToGlobal(pos))
        
        
        
    def reinitSorters(self):
        print "reinitSorters"
        self.ui.cb_sort_client_2.blockSignals(True)
        self.ui.cb_sort_fourniss.blockSignals(True)
        self.ui.cb_marchandise.blockSignals(True)
        self.ui.cb_sort_year.blockSignals(True)
        self.ui.cb_sort_client_2.setCurrentIndex(0)
        self.ui.cb_sort_fourniss.setCurrentIndex(0)
        self.ui.cb_marchandise.setCurrentIndex(0)
        self.ui.cb_sort_year.setCurrentIndex(0)
        self.ui.cb_sort_client_2.blockSignals(False)
        self.ui.cb_sort_fourniss.blockSignals(False)
        self.ui.cb_marchandise.blockSignals(False)
        self.ui.cb_sort_year.blockSignals(False)
        self.updateCtrList()
        
        
    def showCtrNotes(self):
        contract_selected = self.getSelectedContract()
        window = QtGui.QDialog()
        buttons = QtGui.QDialogButtonBox( QtGui.QDialogButtonBox.Cancel | QtGui.QDialogButtonBox.Ok, QtCore.Qt.Horizontal, self)
        buttons.button(QtGui.QDialogButtonBox.Cancel).setText("Fermer")
        buttons.button(QtGui.QDialogButtonBox.Ok).setText("Enregistrer")
        mainLayout = QtGui.QVBoxLayout()
        w_notes = QtGui.QTextEdit()
        w_notes.setText(contract_selected.notes)
        mainLayout.addWidget(w_notes)
        mainLayout.addWidget(buttons)
        window.setLayout(mainLayout)

        buttons.rejected.connect(window.reject)
        buttons.accepted.connect(window.accept)
        
        result = window.exec_()
        if result == QtGui.QDialog.Accepted:
            contract_selected.notes = w_notes.toPlainText()
            self.cDB.updateContract(contract_selected)
        window.close()
        
        
    @QtCore.Slot()
    def openPdfContract(self):
        contract_selected = self.getSelectedContract()
        if contract_selected is not None:
            ctr_path = QtCore.QFileInfo(getFromConfig("path", "words_contract")).absoluteFilePath()
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
        self.s_addDelivery.emit(self.getSelectedContract())
        
        
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
        
        editor.resize(980, 970)
#        QtCore.QObject.connect(contract_editor, QtCore.SIGNAL('s_close_widget'), editor.close)
        contract_editor.s_close_widget.connect(editor.close)
        
        editor.show()
    def closeEditor(self):
        print "received"        
        
    @QtCore.Slot()
    def printContract(self):
        try:
            self.printer.launch(self.getSelectedContract())
        except Exception as e:
            print e
            msgBox = QtGui.QMessageBox()
            msgBox.setText("Une erreur est arrivée lors de l'édition du contrat !")
            msgBox.setStandardButtons(QtGui.QMessageBox.Ok)
            return msgBox.exec_()
        
        
    @QtCore.Slot()
    def removeContract(self):
        ctr = self.getSelectedContract()
        if ctr is not None:
            message = "Êtes-vous sûr de vouloir supprimer définitivement le contrat n°"+str(ctr.n_contrat)+" ?"
            reply = QtGui.QMessageBox.question(self, 'Attention', message, QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
            if reply == QtGui.QMessageBox.Yes:
#                threading.Thread(target=self.cDB.removeContract, args=(ctr,None,)).start()
                self.cDB.removeContract(ctr)
        else:
#            threading.Thread(target=self.cDB.removeContract, args=(ctr,None,)).start()
            self.cDB.clearBDD()
    
    @QtCore.Slot()
    def itemSelected(self):
#        modifiers = QtGui.QApplication.keyboardModifiers()
#        if modifiers == QtCore.Qt.ControlModifier:
#            self.t_ctr_list.setSelectionMode( QtGui.QAbstractItemView.MultiSelection ) 
#        else:
#            self.t_ctr_list.setSelectionMode( QtGui.QAbstractItemView.SingleSelection ) 
        pass
        
    
    def updateOrdererYear(self):
        self.ui.cb_sort_year.blockSignals(True)
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
                
        self.ui.cb_sort_year.clear()
        self.ui.cb_sort_year.addItem("Année", userData = None)
        for y in range(y_min, y_max+1, 1):
            self.ui.cb_sort_year.addItem(str(y), userData = y)
        
        index = self.ui.cb_sort_year.findText(str(datetime.datetime.now().year))
        if index < 0: index = 0
        self.ui.cb_sort_year.setCurrentIndex(index)
        self.ui.cb_sort_year.blockSignals(False)
        self.ui.cb_sort_year.currentIndexChanged.emit(index)
        
        
    def initOrdererFourniss(self):
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
        
    def initOrdererClient(self):
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
        
        
    def initCtrList(self):
        font = self.t_ctr_list.header().font()
        font.setPointSize(10)
        
        col1 = "Date".decode('utf-8').strip()
        col2 = "N°contrat".decode('utf-8').strip()
        col3 = "N°fournisseur".decode('utf-8').strip()
        col4 = "Client".decode('utf-8').strip()
        col5 = "Fournisseur".decode('utf-8').strip()
        col6 = "Modalité".decode('utf-8').strip()
        col7 = "Marchandise".decode('utf-8').strip()
        col8 = "Prix".decode('utf-8').strip()
        col9 = "Qte (T)".decode('utf-8').strip()
        col10 = "Échéancier".decode('utf-8').strip()
        col11 = "À livrer (T)".decode('utf-8').strip()
        col12 = "N°client".decode('utf-8').strip()
        col13 = "Courtage".decode('utf-8').strip()
        col14 = "À payer".decode('utf-8').strip()
        headers = [col1, col2, col3, col4, col5, col6, col7, col8, col9, col10, col11, col12, col13, col14]
        
        self.t_ctr_list.setHeaderLabels(headers)
        self.t_ctr_list.setSortingEnabled(True)
        self.t_ctr_list.header().setResizeMode(QtGui.QHeaderView.ResizeToContents)
        self.t_ctr_list.header().setResizeMode(QtGui.QHeaderView.Interactive)
        self.t_ctr_list.header().setFont( font )
        for i in range(0, len(headers), 1):
            self.t_ctr_list.headerItem().setTextAlignment(i, QtCore.Qt.AlignCenter)
        
        col1 = "Qte totale (T)".decode('utf-8').strip()
        col2 = "Total à livrer (T)".decode('utf-8').strip()
        col3 = "Total à payer (€)".decode('utf-8').strip()
        headers = [col1, col2, col3]
        
        self.ui.t_ctr_total.setHeaderLabels(headers)
        self.ui.t_ctr_total.header().setFont( font )
        width = self.ui.t_ctr_total.parent().sizeHint().width()
        for i in range(0, len(headers), 1):
            self.ui.t_ctr_total.headerItem().setTextAlignment(i, QtCore.Qt.AlignCenter)
            self.ui.t_ctr_total.header().resizeSection(i, width/3)
        self.ui.t_ctr_total.header().setStretchLastSection(True)
            
        self.updateCtrList()
        self.ui.t_ctr_total.header().setResizeMode(QtGui.QHeaderView.ResizeToContents)
        self.ui.t_ctr_total.header().setResizeMode(QtGui.QHeaderView.Interactive)
        
        
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
        curframe = inspect.currentframe()
        calframe = inspect.getouterframes(curframe, 2)
        print "updateCtrList called by ", calframe[1][3]
        
        self.t_ctr_list.clear()
        if ctr_list is None or isinstance(ctr_list, list) == False:
            ctr_list = self.sortContractList()
        
        font = ImageFont.truetype('times.ttf', 12)
        itemlist = []
        for ctr in ctr_list:
            if ctr is None:
                continue
                itemlist = [' - ', ' - ', ' - ', ' - ', ' - ', ' - ', ' - ', ' - ', ' - ', ' - ', ' - ']
            else:
                
                if not hasattr(ctr, "descr_livraison") : 
                    setattr(ctr, "descr_livraison", "")
                    self.cDB.updateContract(ctr)
                
                
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
                monnaie = ' '+getFromConfig('monnaie', 'monnaies')[ctr.monnaie]['sym'].encode('utf8')
        
                nom_client = ctr.getClientName(shortest=True).upper() + "<br/>" +"<i>"+ ctr.get_uVilleAcheteur() + "</i>"
                nom_fourniss = ctr.getFournissName(shortest=True).upper() + "<br/>" +"<i>"+ ctr.get_uVilleVendeur()+ "</i>"

                if ctr.is_franco:
                    modalite = "Franco <br/>"
                else:
                    modalite = "Départ <br/>"
                modalite += ctr.getVilleCible()

                itemlist = []
                itemlist.append(ctr.date_contrat)
                itemlist.append(ctr.n_contrat)
                itemlist.append(ctr.n_fourniss)
                itemlist.append(nom_client)
                itemlist.append(nom_fourniss)
                itemlist.append(modalite)
                itemlist.append(full_marchandise)
                itemlist.append(format_num(ctr.prix)+monnaie)
                itemlist.append(format_num(ctr.qte_total))
                itemlist.append("")
                itemlist.append(format_num(ctr.reste_livraison))
                itemlist.append(ctr.n_client)
                if '%' in ctr.courtage:
                    itemlist.append(format_num(ctr.courtage)+' %')
                else:
                    itemlist.append(format_num(ctr.courtage)+' €')
                itemlist.append(format_num(ctr.reste_paiement)+monnaie)
                
            blankItemlist = list(re.sub(r"<[^>]*>",r'', s.replace("<br/>", '\n')) for s in itemlist)
    
            newLine = TreeWidgetContract(self.t_ctr_list, ctr, blankItemlist)
            for i in range(0, len(itemlist)):
                item = itemlist[i]
                self.t_ctr_list.setItemWidget(newLine, i, TreeWidgetItemLabel(self, item))
                
            self.t_ctr_list.setItemWidget(newLine, 9, DeliveriesViewer(self, ctr))
#            
        self.t_ctr_list.header().setResizeMode(QtGui.QHeaderView.ResizeToContents)
        self.t_ctr_list.header().setResizeMode(QtGui.QHeaderView.Interactive)
        for i in range(0, len(itemlist), 1):
            self.t_ctr_list.resizeColumnToContents(i)
        self.t_ctr_list.header().setResizeMode(self.t_ctr_list.columnCount()-3, QtGui.QHeaderView.Stretch)
#        self.repaint()
        self.updateTotal(ctr_list)
    
    
    def updateTotal(self, ctr_list):
        qte_totale = 0.0
        tot_a_livrer = 0.0
        tot_a_payer = 0.0
        self.ui.t_ctr_total.clear()
        
        for ctr in ctr_list:
            qte_totale += float(format_num(ctr.qte_total))
            tot_a_livrer += float(format_num(ctr.reste_livraison))
            tot_a_payer += float(format_num(ctr.reste_paiement))
            
        newLine = QtGui.QTreeWidgetItem(self.ui.t_ctr_total, [""]*3)
        self.ui.t_ctr_total.setItemWidget(newLine, 0, TreeWidgetItemLabel(self, str(qte_totale)))
        self.ui.t_ctr_total.setItemWidget(newLine, 1, TreeWidgetItemLabel(self, str(tot_a_livrer)))
        self.ui.t_ctr_total.setItemWidget(newLine, 2, TreeWidgetItemLabel(self, str(tot_a_payer)))
        
        height = self.ui.t_ctr_total.visualItemRect(newLine).height()
        width = self.ui.t_ctr_total.parent().sizeHint().width()
        self.ui.t_ctr_total.setFixedHeight(height*2+1)
        
        self.ui.t_ctr_total.header().resizeSection(0, width/3)
        self.ui.t_ctr_total.header().resizeSection(1, width/3)
        self.ui.t_ctr_total.header().resizeSection(2, width/3)
        
        
        
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
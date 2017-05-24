# -*- coding: utf-8 -*-
"""
Created on Wed Feb 22 09:37:14 2017

@author: Raph
"""

#pyside-uic mainwindow.ui -o mainwindow.py


from PySide import QtCore, QtGui
import sys

from classes import Market
from classes import ContractsDatabase

from contract_editor import ContractEditor
from ui_contract_initer import Ui_MainWindow as Ui_ContractIniter

QtCore.QTextCodec.setCodecForCStrings(QtCore.QTextCodec.codecForName("utf-8"))

class UsineLabel(QtGui.QLabel):
    s_usine_selected = QtCore.Signal()
    
    def __init__(self, parent, usine):

        self.usine = usine
        if usine is not None:
            text = '<table width="100%" height="100%">'
            # Adress on left
            text += '<td width="50%"><font size=5><b>'+self.usine.proprietaire.nom+'</b></font><br>'
            text += '<font size=4><i><b>Adresse : </b></i></font><br>'
            for i in range(0, len(self.usine.adresse), 1):
                text += '<font size=3>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'+self.usine.adresse[i]+'</font><br>'
            text += '</td>'
            # Pdts on right
            text += '<td width="50%"><br><br><font size=4><i><b>Produits suivis : </b></i></font><br>'
            for p in self.usine.produits:
                text += '<font size=3>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'+p+'</font><br>'
            text += '</td>'
            text += '</table>'
            
        else:
            text = ""
            print "ERROR LOADING USINE"
        QtGui.QLabel.__init__(self, text)
        super(UsineLabel, self).setStyleSheet("QLabel { border: 1px solid black; }")
        
        self.steelsheet = {'border_width':"1px", 'background_color': "transparent"}
        self.is_selected = False
        
        
    def selected(self):
        self.steelsheet['border_width'] = "3px"
        self.is_selected = True
        self.udateStyleSheet()
        
    def unselected(self):
        self.steelsheet['border_width'] = "1px"
        self.steelsheet['background_color'] = "transparent"
        self.is_selected = False
        self.udateStyleSheet()
        
    def enterEvent(self, ev):
        self.steelsheet['background_color'] = "grey"
        self.udateStyleSheet()
        
    def leaveEvent(self, ev):
        if not self.is_selected:
            self.steelsheet['background_color'] = "transparent"
            self.udateStyleSheet()
        
    def udateStyleSheet(self, stylesheet = None):
        super(UsineLabel, self).setStyleSheet("QLabel {border: "+self.steelsheet['border_width']+" solid black; background-color:"+self.steelsheet['background_color']+";}")
        
    def mouseReleaseEvent(self, ev):
        self.emit(QtCore.SIGNAL('s_usine_selected()'))



class ContractIniter(QtGui.QMainWindow, QtCore.QObject):

    s_go_accueil = QtCore.Signal()
    enter_key_pressed = QtCore.Signal()
        
    def __init__(self, parent=None):
        super(ContractIniter, self).__init__(parent)
        self.ui = Ui_ContractIniter()
        self.ui.setupUi(self)
        
        
        self.contractEditor = ContractEditor(self)
        self.contractEditor.initEditor()
        self.ui.tab_main.addTab(self.contractEditor, "Nouveau contrat")
        self.setWindowTitle("Créateur de contrat")
        
        self.oil_market = Market()
        self.cDB = ContractsDatabase()
        
        self.usine_selected = None
        self.m_completer = QtGui.QCompleter(self.oil_market.marchandises_list['fr'])
        self.m_completer.setCaseSensitivity(QtCore.Qt.CaseInsensitive)
        self.m_completer.setCompletionMode(QtGui.QCompleter.UnfilteredPopupCompletion)
        self.ui.produit.setCompleter(self.m_completer)
        
        
        self.ui.tab_main.setCurrentIndex(0)
        
        self.contractEditor.s_contract_validated.connect(self.close)
        self.contractEditor.s_close_widget.connect(self.close)
        self.connectionsManager(disconnect=False)
        
        self.ui.rb_fournisseur.setChecked(True)
        self.resetPage()
        
        
    def connectionsManager(self, disconnect = False):
        if disconnect == False:
            connector = QtCore.QObject.connect
        else:
            connector = QtCore.QObject.disconnect
            
            
        connector(self.ui.rb_acheteur, QtCore.SIGNAL ('toggled(bool)'), self.resetResult)
        self.ui.produit.textEdited.connect(self.productNameEdited)
#        connector(self.ui.produit, QtCore.SIGNAL ('textEdited(QString)'), self.productNameEdited)
        connector(self.ui.cb_classifier, QtCore.SIGNAL ( 'currentIndexChanged(int)'), self.resultClassifier)
        connector(self.ui.b_rechercher, QtCore.SIGNAL ('clicked()'), self.launchSimulation)
        connector(self.ui.b_next, QtCore.SIGNAL ('clicked()'), self.validateSimulation)
        connector(self.ui.b_reset_simul, QtCore.SIGNAL ( 'clicked()'), self.resetPage)
        
    @QtCore.Slot(str)
    def productNameEdited(self, text):
        print "productNameEdited"
        self.resetResult()
        
    


    @QtCore.Slot()
    def launchSimulation(self):
        condition = 2
        if not (self.ui.rb_acheteur.isChecked() or self.ui.rb_fournisseur.isChecked()):
            self.ui.gb_type.setStyleSheet("#gb_type { border: 3px solid red; }")
            condition = condition - 1
        else:
            self.ui.gb_type.setStyleSheet("")
            
        if len(self.ui.produit.text()) < 1:
            self.ui.produit.setStyleSheet("#produit { border: 3px solid red; }")
            condition = condition - 1
        else:
            self.ui.produit.setStyleSheet("")
            
        if condition < 2:
            return 
            
        self.freeLayout(self.ui.result_layout)
        clients = self.oil_market.get_clients_from_marchandise(self.ui.produit.text(), is_fournisseur=self.ui.rb_fournisseur.isChecked(), enlarge = self.ui.cb_enlarge.isChecked())
#        print clients
        clients = self.ordonnateResult(clients)
        
        if len(clients) > 0 :
            for c in clients :
                u = UsineLabel(self.ui.result_layout, c)
                self.ui.result_layout.addWidget(u)
                QtCore.QObject.connect(u, QtCore.SIGNAL ('s_usine_selected()'), self.simulResultSelected)
        else :
            self.ui.result_layout.addWidget(QtGui.QLineEdit("Aucun client trouve.\n Verifiez la marchandise demandee et/ou la base de donnees."))

    
    @QtCore.Slot(str)
    @QtCore.Slot(bool)
    def resetResult(self, text = None):
        self.freeLayout(self.ui.result_layout)
        self.repaint()
        
    @QtCore.Slot(int)
    def resultClassifier(self, index):
        sender = self.sender()
        if str(sender.currentText()).lower() == "conteneur":
            print(str(sender.currentText()))
            
            
                    
    @QtCore.Slot()
    def simulResultSelected(self):
        print "simulResultSelected"
        
        #catch sender
        sender = self.sender()
        self.usine_selected = (sender.usine, self.ui.rb_acheteur.isChecked())
        # update visually labels
        clients_label_list = self.ui.gb_result.findChildren(UsineLabel)
        for child in clients_label_list:
            if child is not sender:
                child.unselected()
            else:
                child.selected()
        self.ui.b_next.setEnabled(True)

                
    @QtCore.Slot()
    def validateSimulation(self):
        if self.usine_selected is None:
            self.ui.gb_result.setStyleSheet("#gb_result { border: 3px solid red; }")
            return
        else:
            self.ui.gb_result.setStyleSheet("")
            
        if self.contractEditor.new_contract is not None:
            if self.cDB.isCtrLocked(self.contractEditor.new_contract) is False:
                res = self.popupValidation()
                if res == 0:
                    return
                elif res == 1:
                    new_contract = self.contractEditor.new_contract
                elif res == 2:
                    new_contract = self.cDB.newContract()
            else:
                new_contract = self.contractEditor.new_contract
        else:
            new_contract = self.cDB.newContract()
                
        if self.usine_selected[1] == 0: #usine vendeur
            new_contract.usine_depart = self.usine_selected[0]
        else:
            new_contract.usine_destination = self.usine_selected[0]
        new_contract.marchandise = self.ui.produit.text()
            
        self.contractEditor.initEditor(new_contract)
        self.ui.tab_main.setCurrentIndex(1)
        
        
    @QtCore.Slot()
    def resetPage(self):
        self.connectionsManager(disconnect=True)
        self.ui.b_next.setEnabled(False)
        self.ui.produit.clear()
        self.freeLayout(self.ui.result_layout)
        self.usine_selected = None
#        self.initSimulation()
        self.connectionsManager(disconnect=False)
        
        
    @QtCore.Slot()
    def goBack(self):
        self.s_go_accueil.emit()
        
    def popupValidation(self):
        msgBox = QtGui.QMessageBox()
        msgBox.setText("Avant de continuer : ")
        msgBox.setInformativeText("Souhaitez-vous initier un nouveau contrat ? ou modifier le courant ?")
        b_nouveau_ctr = msgBox.addButton(self.tr("Nouveau"), QtGui.QMessageBox.ActionRole)
        b_cancel = msgBox.addButton(self.tr("Annuler"), QtGui.QMessageBox.ActionRole)
        b_maj_ctr = msgBox.addButton(self.tr("Modifier"), QtGui.QMessageBox.ActionRole)
        
        msgBox.setDefaultButton(b_nouveau_ctr)
        
        msgBox.exec_()
        if msgBox.clickedButton() == b_cancel:
            return 0
        elif msgBox.clickedButton() == b_maj_ctr:
            return 1
        elif msgBox.clickedButton() == b_nouveau_ctr:
            return 2
                
    
    def ordonnateResult(self, client_list):
        if str(self.ui.cb_classifier.currentText()).lower() == "pays":
            return sorted(client_list, key = lambda p: p.country_code )
        elif str(self.ui.cb_classifier.currentText()).lower() == "conteneur":
            pass
        return client_list
            
        
    def freeLayout(self, layout):
        for i in reversed(range(layout.count())): 
            widgetToRemove = layout.itemAt( i ).widget()
            layout.removeWidget( widgetToRemove )
            widgetToRemove.setParent( None )
    
    def keyPressEvent(self, e):
        if e.key() == QtCore.Qt.Key_Return or e.key() == QtCore.Qt.Key_Enter:
            self.launchSimulation()
    
    
    def closeEvent(self, event):
        
        current_contract = self.contractEditor.new_contract
        
        print "initer asked to close... ctr is ", current_contract
#        if current_contract is not None:
#            ctr = self.cDB.getContractsByNum(current_contract.n_contrat, True)
#            if ctr is None:
#                self.cDB.cancelContract(current_contract)
                
        if current_contract is not None:# and self.cDB.isCtrLocked(current_contract):
            message = "Êtes-vous sûr de vouloir annuler le contrat en cours d'édition ?"
            
            reply = QtGui.QMessageBox.question(self, 'Attention', message, QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
            if reply == QtGui.QMessageBox.Yes:
                self.cDB.cancelContract(current_contract)
#                self.s_close_widget.emit()
                event.accept() # let the window close
            else:
                event.ignore()
#        else:
#            self.s_close_widget.emit()
            
        print "tout doit se fermer"
#        self.contractEditor.close()

            
    def closeWindow(self):
#        self.contractEditor.close()
        self.close()
        
                
    def main(self):
        self.setWindowIcon(QtGui.QIcon('icone.png'))
        self.setWindowTitle('Gestionnaire de clients')
        self.show()
#        self.showFullScreen()
#        self.showMaximized()
    
if __name__ == "__main__":
    try:
        app = QtGui.QApplication(sys.argv)
    except:
        pass
    mySW = ContractIniter()
    mySW.main()
    sys.exit(app.exec_())
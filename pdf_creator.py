# -*- coding: utf-8 -*-
"""
Created on Mon Mar 27 16:40:43 2017

@author: Raph
"""

from PySide import QtCore, QtGui
import sys
import re
from os import startfile

from ui_printer import Ui_ui_printer as Ui_printer
from utils import getFromConfig
from classes import Market

        

from docxtpl import DocxTemplate, R
from num2words import num2words



class FacturationSelection(QtGui.QDialog): #QtGui.QTreeWidget):
    def __init__(self, parent, adressList):
        super(FacturationSelection, self).__init__(parent)
        self.setWindowTitle("Choix de l'adresse")
        
        self.tree = QtGui.QTreeWidget()
        self.tree.setHeaderLabel("Adresses de facturation possibles :")
        self.tree.setIndentation(0)
#        treeWidget->header() ->close ()
        self.buttons = QtGui.QDialogButtonBox(QtGui.QDialogButtonBox.Ok, QtCore.Qt.Horizontal, self)
        
        self.mainLayout = QtGui.QVBoxLayout()
        self.mainLayout.addWidget(self.tree)
        self.mainLayout.addWidget(self.buttons)
        self.setLayout(self.mainLayout)
        
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)
        
        for adress in adressList:
            QtGui.QTreeWidgetItem(self.tree, [adress])
            
        self.tree.itemAt(0, 0).setSelected(True)
        
    @staticmethod
    def getFacturationAdress(parent = None, adresses = []):
        dialog = FacturationSelection(parent, adresses)
        dialog.resize(500, 500)
        dialog.exec_()
        return dialog.tree.currentIndex().row()
        
    
class langueRB(QtGui.QRadioButton):
    def __init__(self, parent = None, text = "", data = None):
        super(langueRB, self).__init__(text)
        self.data = data
   
    
class policyEdition(QtGui.QDialog):
    def __init__(self, parent = None):
        super(policyEdition, self).__init__(parent)
        
        mainLayout = QtGui.QVBoxLayout()
        layout = QtGui.QHBoxLayout()
        self.fontSelector = QtGui.QFontComboBox()
        self.fontSelector.setEditable(False)
        self.policy = None
        
        self.label = QtGui.QLabel()
        self.label.setFont(self.fontSelector.currentFont())
        self.label.setText("Police courante !")
        
        layout.addWidget(self.fontSelector)
        layout.addWidget(self.label)
        
        self.buttons = QtGui.QDialogButtonBox( QtGui.QDialogButtonBox.Cancel | QtGui.QDialogButtonBox.Ok, QtCore.Qt.Horizontal, self)
        self.buttons.button(QtGui.QDialogButtonBox.Ok).setText("Valider")
        self.buttons.button(QtGui.QDialogButtonBox.Cancel).setText("Annuler")
        
        mainLayout.addLayout(layout)
        mainLayout.addWidget(self.buttons)
        self.setLayout(mainLayout)
        
        QtCore.QObject.connect(self.fontSelector, QtCore.SIGNAL('currentIndexChanged(int)'), self.fontSelected)

        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)
        
    @QtCore.Slot(int)
    def fontSelected(self):
        sender = self.sender()
        index = sender.currentIndex()
        font = sender.itemData(index, QtCore.Qt.DisplayRole)
        self.fontSelector.setCurrentFont(font)
        self.label.setFont(font)
        self.policy = self.fontSelector.currentFont()
        self.label.repaint()
        
    @staticmethod
    def getFont(parent = None):
        dialog = policyEdition(parent)
        result = dialog.exec_()
        if result == QtGui.QDialog.Accepted:
            return dialog.policy.family()
        else:
            return None
        




class PDFCreator(QtGui.QMainWindow, QtCore.QObject):
    s_printed = QtCore.Signal(str)
    
    def __init__(self, parent = None):
        super(PDFCreator, self).__init__(parent)
        self.ui = Ui_printer()
        self.ui.setupUi(self)
        self.setWindowTitle('Édition du document')
        self.oil_market = Market()
        
        self.lang_list = getFromConfig("langages", 'lang_list')
        for lang in self.lang_list:
            rb = langueRB(parent=self.ui.layout_langues, text=lang['nom'], data=lang)
            self.ui.layout_langues.addWidget(rb)
        
        for i in range(0, self.ui.layout_langues.count(), 1):
            w = self.ui.layout_langues.itemAt(i)
            if w is not None:
                w.widget().setChecked(True)
                break
            
        self.setAttribute(QtCore.Qt.WA_StyledBackground)
        self.ui.b_print.clicked.connect(self.createPDF)
        self.ui.b_close.clicked.connect(self.close)
        self.hide()
        
    def launch(self, ctr):
        self.ctr = ctr
        self.show()
        
        
    @QtCore.Slot()
    def createPDF(self, is_fourniss = False, filedir = None, tpl_path = None):
        
        self.hide()
        
        data_path = getFromConfig('path', 'data_dir')
        base_tpl_path = data_path+'Templates/'
        words_path = getFromConfig('path', 'words_contract')
        
        for i in range(0, self.ui.layout_langues.count()):
            widget = self.ui.layout_langues.itemAt(i).widget() 
            if widget!=0 and isinstance(widget, langueRB):
                if widget.isChecked():
                    langue_data = widget.data
                    
        if tpl_path is None:
            filters = "MS Word Documents (*"+langue_data["code"]+".docx)"
            selected_filter = "MS Word Documents (*"+langue_data["code"]+".docx)"
            options = QtGui.QFileDialog.ExistingFiles
            tpl_path = QtGui.QFileDialog.getOpenFileName(self, "Selectionnez un template", base_tpl_path, filters, selected_filter, options)[0]
            if tpl_path is None or tpl_path == "":
                return
            
        filename = self.ctr.n_contrat

        
        #################################################
        ##             NUMERO de CONTRAT             ##
        #################################################
        n_ctr = self.ctr.n_contrat
        
        #################################################
        ##               DATE CONTRAT                  ##
        #################################################
        date_ctr = self.ctr.date_contrat
        
        #################################################
        ##             VILLE DE LVR/CHARG              ##
        #################################################
        if self.ctr.ville is not None and len(self.ctr.ville)>0:
            ville = self.ctr.ville
        else:
            ville = "<VILLE>"
        
        #################################################
        ##             ADRESSE  FACTURATION            ##
        #################################################
        if is_fourniss is True:
            adr_fact = self.ctr.getFactFourniss()
        elif is_fourniss:
            adr_fact = self.ctr.getFactClient()
            
        if isinstance(adr_fact, list):
            adr_fact = adr_fact[FacturationSelection.getFacturationAdress(self, adr_fact)]
        tab_adr_fact = '\t\t\t\t\t\t\t\t'
        adr_fact = adr_fact.replace('\n', '\n'+tab_adr_fact)
        
        
        #################################################
        ##             ADRESSE  CLIENT                 ##
        #################################################
        adr_client = self.ctr.getAdr_uClient()
        if langue_data['code'] != 'fr' and len(re.findall("\\n\w+$", adr_client)) > 0:
            print "ETRANGER, ", adr_client
            pays = re.findall("\\n\w+$", adr_client)[0]
            print "PAYS, ", pays
            adr_client = adr_client.replace(pays, pays.replace("\n", "\t\t\t"))
            print "NEW adr, ", adr_client
        tab_adr_client = '\t\t\t'
        adr_client = adr_client.replace('\n', '\n'+tab_adr_client)
        
        #################################################
        ##                 TVA  CLIENT                 ##
        #################################################
        tva_client = self.ctr.getTVA_uClient()
            
        #################################################
        ##             ADRESSE  FOURNISSEUR            ##
        #################################################
        adr_fourniss = self.ctr.getAdr_uFourniss()
        if langue_data['code'] != 'fr' and len(re.findall("\\n\w+$", adr_fourniss)) > 0:
            pays = re.findall("\\n\w+$", adr_fourniss)[0]
            adr_fourniss = adr_fourniss.replace(pays, pays.replace("\n", "\t\t\t"))
        tab_adr_fourniss = '\t\t\t'
        adr_fourniss = adr_fourniss.replace('\n', '\n'+tab_adr_fourniss)
        
        #################################################
        ##                 TVA  FOURNISSEUR            ##
        #################################################
        tva_fourniss = self.ctr.getTVA_U_Fourniss()
            
        #################################################
        ##                MARCHANDISE                  ##
        #################################################
#        m_nom = self.ctr.marchandise.decode('utf-8')
        m_nom = self.oil_market.getMarchandiseFullName(self.ctr.marchandise, langue_data['code'])
#        marchandise_list = self.oil_market.marchandises_list[langue_data['code']]
#        m_nom = marchandise_list[self.ctr.marchandise]#.decode('utf-8')
        m_quantite = self.ctr.quantite
        
        if self.ctr.unite == 'kg':
            if langue_data['code'] == 'fr':
                m_unite = 'le '
            elif langue_data['code'] == 'en':
                m_unite = 'per '
            elif langue_data['code'] == 'es':
                m_unite = 'el '
            m_unite += langue_data['kg_unite']
        elif self.ctr.unite == 't':
            if langue_data['code'] == 'fr':
                m_unite = 'la '
            elif langue_data['code'] == 'en':
                m_unite = 'per '
            elif langue_data['code'] == 'es':
                m_unite = 'la '
            m_unite += langue_data['t_unite']
        
        #################################################
        ##                  PAIEMENT                   ##
        #################################################
        
        str_prix = self.ctr.prix
        matches = re.findall(r"[-+]?\d*\.*\d+", str_prix)
        if len(matches) > 0:
            prix_num = matches[0]
            prix_words = num2words(float(prix_num), lang=langue_data['code'])
        else:
            prix_num = str_prix
            prix_words = ""
            
        if self.ctr.monnaie == 0:
            monnaie = u'\u20ac'.encode('utf8')
            prix_words += ' euros'
        elif self.ctr.monnaie == 1:
            monnaie = u'\u00a3'.encode('utf8')
            prix_words += ' dollars'
        elif self.ctr.monnaie == 2:
            monnaie = u'\u0024'.encode('utf8')
            prix_words += ' livres'
        else:
            monnaie = ""
            
        if len(self.ctr.paiement) > 0:
            index = self.oil_market.paiements["fr"].index(self.ctr.paiement)
            paiement = self.oil_market.paiements[langue_data['code']][index]
            courtage = self.ctr.courtage
        else:
            paiement = ""
            courtage = ""

            
        #################################################
        ##                 LIVRAISON                   ##
        #################################################
        dlv_dic = self.ctr.periode_livraison
        periode_livraison = ""
        
        month_names = langue_data['months']
        ordered_years = sorted(dlv_dic.keys())
        for i in range(0, len(ordered_years), 1):
            if len(periode_livraison) > 0 :
                periode_livraison += '\n'
            y = ordered_years[i]
            for j in range(0, 12):
                m = month_names[j]
                total = int(float(dlv_dic[y][str(j+1).zfill(2)]["total"]))
                if total == 0: continue
                if len(periode_livraison) > 0 :
                    periode_livraison += ', '+m
                else:
                    periode_livraison += m
            periode_livraison += ' - '+str(y)
                
        if len(self.ctr.logement) > 0:
            index = self.oil_market.logements["fr"].index(self.ctr.logement)
            format_livraison = self.oil_market.logements[langue_data['code']][index]
        else:
            format_livraison = ""
        
        if self.ctr.is_franco is True:
            if langue_data['type_deliv'][1] == "":
                type_deliv = langue_data['type_deliv'][0].lower()
            else:
                type_deliv = langue_data['type_deliv'][1].lower()
        else:
            if langue_data['type_deliv'][3] == "":
                type_deliv = langue_data['type_deliv'][2].lower()
            else:
                type_deliv = langue_data['type_deliv'][3].lower()
        
        has_tva_client = False
        if len(tva_client) > 0:
            tva_client += '\n'
            has_tva_client = True
            
        has_tva_fourniss = False
        if len(tva_fourniss) > 0:
            tva_fourniss += '\n'
            has_tva_fourniss = True
            
        context = { 
            'is_fourniss': is_fourniss,
            'date_ctr' : R(date_ctr, size=24),
            'n_ctr' : R(n_ctr, size=24),
            'adr_fact' : R(adr_fact, size=24),
            'adr_fourniss' : R(adr_fourniss, size=24),
            'tva_fourniss' : R(tva_fourniss, size=24),
            'has_tva_fourniss' : has_tva_fourniss,
            'adr_client' : R(adr_client, size=24),
            'tva_client' : R(tva_client, size=24),
            'has_tva_client' : has_tva_client,
            
            'm_nom' : R(m_nom, size=24),
            'm_quantite': R(m_quantite, size=24),
            'm_unite': R(m_unite, size=24),
            'format_livraison' : R(format_livraison, size=24),
            'date_livraison' : R(periode_livraison, size=24),
            'type_delivery' : R(type_deliv, size=24),
            'ville' : R(ville, size=24),
            
            'monnaie': R(monnaie, size=24),
            'prix_num': R(prix_num, size=24),
            'prix_words': R(prix_words, size=24),
            'paiement': R(paiement, size=24),
            'courtage' : R(courtage, size=24)
        }
        
        if filedir is None:
            filedir = QtGui.QFileDialog.getExistingDirectory(self, "Où enregistrer ?", words_path, QtGui.QFileDialog.ShowDirsOnly | QtGui.QFileDialog.DontResolveSymlinks)
        
        if filedir is None:
            return
        
        if not filedir.endswith('/'):
            filedir += '/'
        
        try:
            ctr = DocxTemplate(tpl_path)
            ctr.render(context)
            if is_fourniss is False:
                ctr_doc = filedir + filename + "_client.docx"
                ctr.save(ctr_doc)
            else:
                ctr_doc = filedir + filename + ".docx"
                ctr.save(ctr_doc)
            
        except Exception as e:
            print e
            msgBox = QtGui.QMessageBox()
            msgBox.setText("Une erreur est arrivée lors de l'édition du contrat !")
            msgBox.setStandardButtons(QtGui.QMessageBox.Ok)
            return msgBox.exec_()
        
        startfile(ctr_doc)
        
        if is_fourniss is False:
            return self.createPDF(is_fourniss=True, filedir=filedir, tpl_path=tpl_path)
        
    
        
if __name__ == "__main__":
    from classes import ContractsDatabase
    
    cDB = ContractsDatabase()
    ctr = cDB.getEveryContracts()[0]
    
    app = QtGui.QApplication(sys.argv)
    cc = PDFCreator()
    cc.launch(ctr)
#    cc.createPDF(None, True)
    
    sys.exit(app.exec_())
        
        
        
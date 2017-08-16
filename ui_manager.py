# -*- coding: utf-8 -*-
"""
Created on Mon Mar 27 16:52:09 2017

@author: Raph
"""

from PySide import QtCore, QtGui
import sys

from ui_accueil import Ui_Accueil
from contract_initer import ContractIniter
from contracts_manager import ContractsManager
from delivery_manager import DeliveryManager

from utils import getFromConfig
from classes import Market

UI_ACCUEIL = 0
#UI_CCREATOR = 2
UI_CTR_MANAGER = 1
UI_DEL_MANAGER = 2


class Ui_manager(QtGui.QMainWindow, QtCore.QObject):
    def __init__(self, version = 0.0, parent = None):
        super(Ui_manager, self).__init__(parent)
        self.ui = Ui_Accueil()
        self.ui.setupUi(self)
        self.setWindowIcon(QtGui.QIcon('icone.png'))
        self.setWindowTitle('Gestionnaire de clientèle')
        self.ui.splitter.setHandleWidth(15)
        self.version = version

        l_ctr = QtGui.QHBoxLayout()
        scroll_ctr = QtGui.QScrollArea()
        self.ctr_manager = ContractsManager(self)
        self.w_ctr = self.ctr_manager.ui.ctr_centralwidget
        self.w_ctr.setAttribute(QtCore.Qt.WA_StyledBackground)
        self.w_ctr.setObjectName("w_ctr")
#        self.w_ctr.adjustSize()
        scroll_ctr.setWidgetResizable(True)
        scroll_ctr.setWidget(self.w_ctr)
#        scroll_ctr.adjustSize()
        l_ctr.addWidget(scroll_ctr)
        self.ui.f_contracts.setLayout(l_ctr)
        self.ui.f_contracts.setFrameShape(QtGui.QFrame.NoFrame)
        
        l_deliv = QtGui.QHBoxLayout()
        scroll_deliv = QtGui.QScrollArea()
        self.dlv_manager = DeliveryManager(self)
        self.w_dlv = self.dlv_manager.ui.dlv_centralwidget
        self.w_dlv.setAttribute(QtCore.Qt.WA_StyledBackground)
        self.w_dlv.setObjectName("w_dlv")
        scroll_deliv.setWidget(self.w_dlv)
        scroll_deliv.setWidgetResizable(True)
        l_deliv.addWidget(scroll_deliv)
        self.ui.f_deliveries.setLayout(l_deliv)
        self.updateStyle()
        
        self.ctr_manager.s_addDelivery.connect(self.dlv_manager.addDelivery)
        
        self.oil_market = Market()
#        self.ctr_manager.FIAUpdated()
#        self.ctr_manager.FIFUpdated()
        self.ui.actionConfig.triggered.connect(self.oil_market.updateConfigLanguages)
        self.ui.actionFIA.triggered.connect(self.updateFIA)
        self.ui.actionFIF.triggered.connect(self.oil_market.updateFIF)
        self.ui.menuA_propos.aboutToShow.connect(self.a_propos)
        
        self.showMaximized()

    def updateStyle(self):
        with open(getFromConfig("path", "stylesheet_file"), 'r') as f:
            style = f.read()
        self.setStyleSheet(style)
        
    def updateFIA(self):
        self.oil_market.updateFIA()
        self.ctr_manager.FIAUpdated()
        
    def updateFIF(self):
        self.oil_market.updateFIA()
        self.ctr_manager.FIFUpdated()
        
    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_F5:
            self.updateStyle()
        elif event.key() == QtCore.Qt.Key_Escape:
            self.ctr_manager.t_ctr_list.clearSelection()
            self.dlv_manager.t_deliver_list.clearSelection()
        elif event.key() == QtCore.Qt.Key_Control:
            self.ctr_manager.t_ctr_list.setSelectionMode( QtGui.QAbstractItemView.MultiSelection ) 
            self.dlv_manager.t_deliver_list.setSelectionMode( QtGui.QAbstractItemView.MultiSelection ) 

            
    def keyReleaseEvent(self, event):
        if event.key() == QtCore.Qt.Key_Control:
            self.ctr_manager.t_ctr_list.setSelectionMode( QtGui.QAbstractItemView.SingleSelection ) 
            self.dlv_manager.t_deliver_list.setSelectionMode( QtGui.QAbstractItemView.SingleSelection ) 

#    def mouseReleaseEvent(self, event):
#        print "Ui_manager mouseReleaseEvent"
            
            
    def a_propos(self):
#        message = "Logiciel développé par\nRaphaël Abelé\n pour\nC.Ciraud & Cie\n\nVersion: "+ str(self.version)
        about = QtGui.QMessageBox(None)
        about.setWindowFlags(  QtCore.Qt.WindowSystemMenuHint | QtCore.Qt.WindowTitleHint )
        about.setWindowTitle("A propos")
        about.setText("<p align='center'>Logiciel développé par<br><b>Raphaël Abelé</b><br>pour<br><b>C.Giraud & Cie</b><br><br>Version : <b>"+str(self.version)+"</b>")
        about.exec_()


    def main(self):
        self.show()
        
if __name__ == "__main__":
    try:
        app = QtGui.QApplication(sys.argv)
    except:
        pass
    mySW = Ui_manager()
    mySW.main()
    sys.exit(app.exec_())
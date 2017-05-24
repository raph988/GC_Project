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
    def __init__(self, parent = None):
        super(Ui_manager, self).__init__(parent)
        self.ui = Ui_Accueil()
        self.ui.setupUi(self)
        self.setWindowIcon(QtGui.QIcon('icone.png'))
        self.setWindowTitle('Gestionnaire de clientèle')
        self.ui.splitter.setHandleWidth(15)

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
        
        self.oil_market = Market()
        self.ui.actionConfig.triggered.connect(self.oil_market.updateConfigLanguages)
        self.ui.actionFIA.triggered.connect(self.updateFIA)
        self.ui.actionFIF.triggered.connect(self.oil_market.updateFIF)
        
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
        self.ctr_manager.FIAUpdated()
        
    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_F5:
            self.updateStyle()
            



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
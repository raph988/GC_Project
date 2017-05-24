# -*- coding: utf-8 -*-
"""
Created on Mon Feb 27 16:24:21 2017

@author: Raph
"""

from utils import _format
from utils import getFromConfig

import openpyxl as pyxl
import win32com.client as wc
import os


NUM_CTR = 0
NUM_CTR_C = 1
NUM_CTR_F = 2

NUM_DLV_CH = 0
NUM_DLV_C = 1
NUM_DLV_F = 2


def usine_parser(sheet, sheet_name):
    
    usines = []
    
    sections = find_sections(sheet)
    
    vendeur = {}
    vendeur['nom'] = sheet.cell(row=1, column=1).value.encode('utf8') #_format(sheet.cell(row=1, column=1).value, set_lower = False, clear = True)
    vendeur['fonction'] = ""
    
    for i in range(2, sheet.max_row, 1):
        cell = sheet.cell(row=i, column=1)
        if is_keyword(cell):
            cell_value = _format(sheet.cell(row=i, column=2).value, set_lower = False, clear = True)
            if type(cell_value).__name__ == 'str' and len(cell_value)>0:
                vendeur['fonction'] = cell_value
#                if len(sections) <= 1:
#                    sections.insert(0, i+1)
                break
    
    s_id = 0
    sections.insert(0, i+1)
    for s_id in range(0, len(sections)-1):
        usine = {}
        areas = find_bounding_rects(sheet, (sections[s_id], sections[s_id+1]))
        if len(areas) < 1 :
            continue
        for area in areas:
            keywords = test_keyword(sheet.cell(row=area[0][0], column=area[0][1]).value)
            values = get_values(sheet=sheet, column=area[0][1]+1, row_start=area[0][0], row_end=area[1][0])
            for key in keywords:
                if key in usine.keys():
#                    pass
                    #####################################################
                    ##                 A DECOMMENTER                   ##
                    #####################################################
                    if isinstance(usine[key][0], list):
                        usine[key].append(values)
                    else:
                        usine[key] = [usine[key]]
                        usine[key].append(values)
                else:
                    usine[key] = values
        usines.append(usine)
        
    vendeur['usines'] = usines
    
#    if 'COUDENE' in vendeur['nom']:
#        for u in vendeur['usines']:
#            print u
                  
    return vendeur
    

def get_values(sheet, column, row_start, row_end):
    values = []
    for i in range(row_start, row_end+1,1):
        cell_value = sheet.cell(row=i, column=column).value
        if cell_value is not None and cell_value is not None:
            values.append(cell_value)
    return values

        
def test_keyword(word):
    keywords = []
    word = _format(word, clear=True, set_lower = True)
    
    if is_facturation_adresse(word):
        keywords.append("adresse facturation")
        
    if is_usine_adresse(word):
        keywords.append("adresse usine")
    
#    if is_siege_adresse(word):
        
    if is_produits(word):
        keywords.append("produits")
        
    if len(keywords) < 1:
        keywords.append(word)
        
        
    return keywords
                    
    
def is_facturation_adresse(key):
    key = key.lower()
    if "adress" in key and "factur" in key:
        return True
    return False
    
def is_usine_adresse(key):
    key = key.lower()
    if ("adress" in key and "usine" in key) or "siege" in key:
        return True
    return False

#def is_siege_adresse(key):
#    key = key.lower()
#    if ("adress" in key and "principale" in key) or "siege" in key:
#        return True
#    return False


def is_produits(key):
    key = key.lower()
    if "produit" in key:
        return True
    return False
    
def find_bounding_rects(sheet, r_limits):
    areas = []
    for i in range(r_limits[0], r_limits[1],1):
        for j in range(1, sheet.max_column+1,1):
            cell = sheet.cell(row=i, column=j)
            if is_keyword(cell):
                areas.append(find_area(sheet, (i, j), r_limits=r_limits))
    return areas
    
def find_sections(sheet):
    sections = []
    for i in range(1, sheet.max_row+1,1):
        cell = sheet.cell(row=i, column=1)
        if is_section_style(cell):
            sections.append(i)
    sections.append(sheet.max_row+1)
    return sections
    
        
def find_area(sheet, pos, r_limits):
    i, j = pos
    area = [[i,j], [i, j]] # tuple is non mutable type
    
    # growth time
    inc_i, inc_j = 1, 1
    while (inc_i != 0 or inc_j != 0) and area[1][0] < r_limits[1] and area[1][1] < sheet.max_column:
        if inc_i != 0:
            next_line = list(sheet.cell(row=area[1][0]+1, column=cg) for cg in range(area[0][1], area[1][1]+1, 1)) 
            for cell in next_line:
                if is_keyword(cell) or is_section_style(cell):
                    inc_i = 0
                    break
                
        if inc_j != 0:
            next_column = list(sheet.cell(row=rg, column=area[1][1]+1) for rg in range(area[0][0], area[1][0]+2, 1))
            for cell in next_column:
                if is_keyword(cell) or is_section_style(cell):
                    inc_j = 0
                    break
        inc_area(area, inc_i, inc_j)
        
#    # wrap time
    inc_i, inc_j = -1, -1
    while (inc_i != 0 or inc_j != 0) and area[1][0] > r_limits[0] and area[1][1] > sheet.min_column:
        
        if inc_i != 0:
            last_line = list(sheet.cell(row=area[1][0], column=cw) for cw in range(area[0][1], area[1][1]+1, 1))
            for cell in last_line:
                if cell.value is not None:
                    inc_i = 0
                    break
                
        if inc_j != 0:
            last_column = list(sheet.cell(row=rw, column=area[1][1]) for rw in range(area[0][0], area[1][0]+1, 1))
            for cell in last_column:
                if cell.value is not None:
                    inc_j = 0
                    break
                    
        inc_area(area, inc_i, inc_j)
    return area

    
def inc_area(area, inc_i, inc_j):
    area[1][0] += inc_i
    area[1][1] += inc_j
#    print "new area is ", area
    
        
        
def is_keyword(cell):
    if cell.font.b == True and cell.font.u == "single" and cell.value is not None:
        return True
    return False
    
def is_section_style(cell):
    if cell.value is not None and cell.font.color is not None and cell.font.color.theme is not None:
        if str(cell.font.color.theme).isdigit() and cell.font.color.theme != 1:
            return True
        
    return False



from PySide import QtGui, QtCore

def ReverseExecutionParser():
    
    from classes import ContractsDatabase
    cDB = ContractsDatabase()
    path = getFromConfig("path", "exec")
    
    wb = pyxl.load_workbook(path)
    
    test = 1
    while test == 1:
        try: 
            wb.save(path)
        except:
            message = 'Fermez le fichier "'+path+'" pour pouvoir poursuivre.'
            QtGui.QMessageBox.question(None,'Attention !' , message, QtGui.QMessageBox.Yes)
        else:
            wb = pyxl.load_workbook(path)
            test = 0
        
    
    sheet = wb.get_sheet_by_name("Planning")
    # on va a la derniere ligne puis on de décalle sur la colonne des num de livraison
    
    last_line = 0
    # on va a la derniere ligne
    for last_line in range(1, sheet.max_row+1, 1):
        cell_value = _format(sheet.cell(row=last_line, column=2).value)
        if cell_value == '':
            break
    #• puis on de décalle sur la colonne des num de livraison pour chercher le dernier ajout 
    for last_registered in range(last_line, 0, -1):
        cell_value = _format(sheet.cell(row=last_registered, column=17).value)
        if cell_value != "":
            break
    
    for i in range(last_registered+1, last_line, 1):
        dic = {}
        
        dic["date_appel"] = sheet.cell(row = i, column=2).value
        dic["client_name"] = sheet.cell(row = i, column=3).value
        dic["fournisseur_name"] = sheet.cell(row = i, column=4).value
        cell = sheet.cell(row = i, column=5).value.lower()
        if 'franco' in cell or 'fr' in cell:
            dic["is_franco"] = True
        else:
            dic["is_franco"] = False
        
        dic["ville"] = sheet.cell(row = i, column=6).value
        dic["date_charg_livr"] = sheet.cell(row = i, column=7).value
        dic["horaire_charg_livr"] = sheet.cell(row = i, column=8).value
        dic["quantite"] = sheet.cell(row = i, column=9).value
        dic["marchandise"] = sheet.cell(row = i, column=10).value
        dic["n_ctr"] = sheet.cell(row = i, column=11).value
        dic["ref_fourniss"] = sheet.cell(row = i, column=12).value
        dic["ref_client"] = sheet.cell(row = i, column=13).value
        dic["ref_chargement"] = sheet.cell(row = i, column=14).value
        cell = sheet.cell(row = i, column=15).value or ""
        if "oui" in cell :
            dic["is_confirmed"] = True
        else:
            dic["is_confirmed"] = False
            
        cell = sheet.cell(row = i, column=16).value
        cell = _format(cell, set_lower=True, clear=True)
        if "paye" in cell or "p" in cell:
            dic["is_paid"] = True
        else:
            dic["is_paid"] = False
           
        if dic["n_ctr"] != "":
            num = dic["n_ctr"]
            type_num = NUM_CTR
            ctr_list = cDB.getContractsByNum(num, type_num)
        elif dic["ref_client"] != "" and len(ctr_list) < 1:
            num = dic["ref_client"]
            type_num = NUM_CTR_C
            ctr_list = cDB.getContractsByNum(num, type_num)
        elif dic["ref_fourniss"] != "" and len(ctr_list) < 1:
            num = dic["ref_fourniss"]
            type_num = NUM_CTR_F
            ctr_list = cDB.getContractsByNum(num, type_num)
        if len(ctr_list) < 1:
            message = "Aucun contrat trouvé sous la réf. "+ str(num) + "."
            QtGui.QMessageBox.question(None, 'Attention',  message, QtGui.QMessageBox.Yes)
            continue
        else:
            ctr = ctr_list[0]
            
        dic["n_livr"] = ctr.n_contrat +"-"+ str(len(ctr.livraisons.keys())).zfill(2)
        sheet.cell(row = i, column=17).value = dic["n_livr"]
        ctr.addDelivery(dic)
        cDB.updateContract(ctr)
            
    wb.save(path)
    

# action 0 new delivery
# action 1 edit delivery
# action 2 edit remove delivery
def ExecutionParser(delivery=None, action = 0):
    
    progressDialog = QtGui.QProgressDialog()
    progressDialog.setAutoClose(False)
    progressDialog.setAutoReset(False)
    label = progressDialog.findChildren(QtGui.QLabel)[0]
    label.setFont(QtGui.QFont("Calibri", 12))
    button = progressDialog.findChildren(QtGui.QPushButton)[0]
    button.hide()
    progressBar = progressDialog.findChildren(QtGui.QProgressBar)[0]
    progressBar.hide()
    
    
    path = getFromConfig("path", "exec")
    
    wb = pyxl.load_workbook(path)
    
    test = 1
    while test == 1:
        try: 
            wb.save(path)
        except:
            message = 'Fermez le fichier "'+path+'" pour pouvoir poursuivre.'
            QtGui.QMessageBox.question(None,'Attention !' , message, QtGui.QMessageBox.Yes)
        else:
            wb = pyxl.load_workbook(path)
            test = 0
        
    
    progressDialog.setWindowTitle(u"Édition en cours...")
    text = u"\n\nÉdition du fichier \n"+path
    progressDialog.setLabelText(text)
    progressDialog.show()
    QtGui.QApplication.processEvents()
    
    
    sheet = wb.get_sheet_by_name("Planning")
    
    i = 0
    if action == 0:
        # on va a la derniere ligne
        for i in range(1, sheet.max_row+1, 1):
            cell_value = _format(sheet.cell(row=i, column=2).value)
            if cell_value == '':
#                print i
                break
    elif action == 1 or action == 2:
        #on cherche le num de livraison
        for i in range(1, sheet.max_row+1, 1):
            cell_value = _format(sheet.cell(row=i, column=17).value)
            if cell_value == delivery.n_livr:
#                print i
                break

    
    if action != 2 and delivery is not None:
        sheet.cell(row = i, column=2).value = delivery.date_appel
        sheet.cell(row = i, column=3).value = delivery.client_name
        sheet.cell(row = i, column=4).value = delivery.fournisseur_name
        if delivery.is_franco: type_livr = "Franco"
        else: type_livr = "Départ"
        sheet.cell(row = i, column=5).value = type_livr
        sheet.cell(row = i, column=6).value = delivery.ville.title()
        sheet.cell(row = i, column=7).value = delivery.date_charg_livr
        sheet.cell(row = i, column=8).value = delivery.horaire_charg_livr
        sheet.cell(row = i, column=9).value = delivery.quantite
        sheet.cell(row = i, column=10).value = delivery.marchandise
        sheet.cell(row = i, column=11).value = delivery.n_ctr
        sheet.cell(row = i, column=12).value = delivery.ref_fourniss
        sheet.cell(row = i, column=13).value = delivery.ref_client
        sheet.cell(row = i, column=14).value = delivery.ref_chargement
        if delivery.is_confirmed: confirmation = "Oui"
        else: confirmation = "Non"
        sheet.cell(row = i, column=15).value = confirmation
        if delivery.is_paid: paiement = "Payé"
        else: paiement = ""
        sheet.cell(row = i, column=16).value = paiement
        sheet.cell(row = i, column=17).value = delivery.n_livr
    elif action == 2 and delivery is not None:
        for j in range(2, 18, 1):
            sheet.cell(row = i, column=j).value = ""

    wb.save(path)

    progressDialog.close()
    QtGui.QApplication.processEvents()
    
    
    progressDialog.setWindowTitle("Ouvertue en cours...")
    text = u"\n\n→ "+path+"\n\n"
    text += u"Si le ficher ne s'ouvre pas, vérifiez qu'il ne le soit pas déjà !"
    progressDialog.setLabelText(text)
    progressDialog.show()
    QtGui.QApplication.processEvents()
    
    try:
        openWorkSheet(path, "Planning", readOnly=False)
    except:
        pass
    
    progressDialog.close()
    QtGui.QApplication.processEvents()
    


def openWorkSheet(workbook_path, worksheet_name, readOnly=True):
    if os.path.exists(workbook_path):
        xl = wc.Dispatch("Excel.Application")
        xl.Workbooks.Open(Filename=workbook_path, ReadOnly=readOnly)
        xl.Worksheets(worksheet_name).Activate()
        xl.Visible = True
        del xl
    else:
        print"file doesnt exist."



import sys
if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
#    fif = "C:/Users/Raph/Documents/Python Scripts/G&Cie/data/fif.xlsx"
#    fia = "C:/Users/Raph/Documents/Python Scripts/G&Cie/data/fia.xlsx"
#
#    wb = load_workbook(fif)
#    sheet = wb.get_sheet_by_name("BROCHENIN")
#    vendeur = usine_parser(sheet, "CARGILL")
#    ExecutionParser(None)
    ReverseExecutionParser()
#    find_area(sheet, (3,1))
#    wb = load_workbook(fia)
#    sheet = wb.get_sheet_by_name("COUDENE")
#    vendeur = parse_usine(sheet, "CARGILL")
#    print vendeur["usines"][0]["adresse"]
    
#    date = datetime.datetime.now()
#    
#    cm = ClientSheetManager()
#    cm.loadSheet("C:/Users/Raph/Documents/Python Scripts/G&Cie/data/aigremont.xlsx", str(date.year))

    print "END"
    app.exec_()
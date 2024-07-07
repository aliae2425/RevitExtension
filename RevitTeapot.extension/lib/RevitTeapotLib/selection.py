# -*- coding: utf-8 -*-

#! python3
from Autodesk.Revit.DB import *
from pyrevit import forms, revit, DB
from collections import defaultdict


activ_document   = __revit__.ActiveUIDocument.Document

pyDoc = revit.DOCS.doc
uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document
app = __revit__.Application

class selection:
    
    def PrintSelection(self):
        print("RevitTeapotLib.Selection loaded")
        
    # def UserSheetSelection(self):
    #     return forms.select_sheets(title="Selectionner les feuilles", button_name="Selectionner")

    # def FormSelector():
    #     ops = ["Porte", "Fenetre"]
    #     floorPlantype = {"Porte": BuiltInCategory.OST_Doors, "Fenetre": BuiltInCategory.OST_Windows}
    #     return( floorPlantype[forms.CommandSwitchWindow.show(ops, message='Selectionner le type de menuiserie')])
    
    # def FilterListByParameter(self, DictItems) :
    #     parameters = []
    #     famille = []
    #     familyType = []
    #     for key, item in DictItems.items():
    #         for para in item.Symbol.Parameters: 
    #             parameters.append(para.Definition.Name)
    #         break
    #     FilterType = forms.CommandSwitchWindow.show(parameters, message='Selectionner le type de parametre')
    #     for i in DictItems :
    #         for para in i.Symbol.Parameters:
    #             if para.Definition.Name == FilterType:
    #                 if para.AsValueString() in familyType:
    #                     famille.append(i)
    #     return famille
# -*- coding: utf-8 -*-

# ------------------------------- info pyrevit ------------------------------- #
__title__ = "Detailer les fenetres"
__doc__ = """
    version : 0.0.1
    Date : 03.03.2024
    __________________
    un bouton pour les detailer toutes 
"""
__author__ = 'Aliae'                               
__min_revit_ver__ = 2024                                       
__max_revit_ver__ = 2025


from Autodesk.Revit.DB import *
from pyrevit import forms


activ_document   = __revit__.ActiveUIDocument.Document

uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document
app = __revit__.Application



class Menuiserie:
    
    def __init__(self, obj):
        self.name = obj.Name
        self.category = obj.Category.Name
        self.origin = obj.Location.Point
        self.vector = obj.Host.Location.Curve.GetEndPoint(0) - obj.Host.Location.Curve.GetEndPoint(1)
        
        self.height = self.setHeight(obj)
        self.width = self.setWidth(obj)
        self.offset = self.depth = UnitUtils.ConvertFromInternalUnits(40, UnitTypeId.Centimeters)
        
        self.element = obj

    def __repr__(self):
        return "menuiserie : {} \n hauteur : {} \n largeur : {} \n".format(self.name, self.height, self.width)

    def setWidth(self, obj):
        value = obj.Symbol.get_Parameter(BuiltInParameter.DOOR_WIDTH).AsDouble()
        if value:
            return value
        else:
            print("❌ la famille n'a pas de parametre de largeur standard")
    def setHeight(self, obj):
        value = obj.Symbol.get_Parameter(BuiltInParameter.GENERIC_HEIGHT).AsDouble()
        if value:
            return value
        else:
            print("❌ la famille n'a pas de parametre de hauteur standard")
            
    def ScopBox(self):
        print(self.element)

        

def getAllElement(category):
    return FilteredElementCollector(doc).OfCategory(category).WhereElementIsNotElementType().ToElements()

def FormSelector():
    ops = ["Porte", "Fenetre"]
    floorPlantype = {"Porte": BuiltInCategory.OST_Doors, "Fenetre": BuiltInCategory.OST_Windows}


    return( floorPlantype[forms.CommandSwitchWindow.show(ops, message='Selectionner le type de menuiserie')])

if __name__ == "__main__":
   
    mainDict = {}
   
    # -------------------------- filter element on wall -------------------------- #
    for i in getAllElement(FormSelector()):
       key = "{}-{}".format(i.Symbol.Family.Name, Element.Name.GetValue(i.Symbol))
       if type(i.Host) == Wall:
           mainDict[key] = i
       else:
           print("❌ L'element {} n'est pas sur un mur ({})".format(key, i.Id))
    
    # ------------------------- detailler les Menuiserie ------------------------- #

    for key, item in mainDict.items():
        print("🔧 Detailer l'element : {}".format(key))
        print(Menuiserie(item))
    
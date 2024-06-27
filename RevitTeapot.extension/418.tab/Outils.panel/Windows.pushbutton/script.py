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
__min_revit_ver__ = 2022                                       
__max_revit_ver__ = 2025


from Autodesk.Revit.DB import *
from pyrevit import forms, revit, DB
from collections import defaultdict


activ_document   = __revit__.ActiveUIDocument.Document

pyDoc = revit.DOCS.doc
uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document
app = __revit__.Application

TITLEBLOCK =  doc.GetDefaultFamilyTypeId(ElementId(BuiltInCategory.OST_TitleBlocks))
OFFSET = 40

class Menuiserie:    
    def __init__(self, obj):
        self.name = obj.Name
        self.ctg = obj.Category.Name
        self.origin = obj.Location.Point
        self.vector = obj.Host.Location.Curve.GetEndPoint(0) - obj.Host.Location.Curve.GetEndPoint(1)
        self.height = self.setHeight(obj)
        self.width = self.setWidth(obj)
        self.offset = UnitUtils.ConvertToInternalUnits(OFFSET, UnitTypeId.Centimeters)
        self.box = BoundingBoxXYZ()
        self.trans = Transform.Identity
    def __repr__(self):
        return "Menuiserie : {} \n\t- hauteur : {} \n\t- largeur : {} \n\t- origine : {}".format(self.name, self.height, self.width, self.origin)
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
    def VectorTransform(self, viewType):
        self.trans.Origin = self.origin
        vector = self.vector.Normalize()
        if viewType != "section":
            self.trans.BasisX = vector
        else:
            self.trans.BasisX = vector.CrossProduct(XYZ.BasisZ)
        
        if viewType == "plan":
            self.trans.BasisY = -XYZ.BasisZ.CrossProduct(vector) 
        else:
            self.trans.BasisY = XYZ.BasisZ
        
        if viewType == "elevation":
                self.trans.BasisZ = vector.CrossProduct(XYZ.BasisZ)
        elif viewType == "section":
                self.trans.BasisZ = vector.CrossProduct(XYZ.BasisZ).CrossProduct(XYZ.BasisZ)
        elif viewType == "plan":
                self.trans.BasisZ = -XYZ.BasisZ
        else:
                print("❌ type de vue non reconnu")               
    def scopeBox(self, type):
        self.box.Min = XYZ(  -self.width/2-self.offset,      -self.offset,               -self.offset/2 )
        if type == "plan":
            self.box.Min = XYZ(  -self.width/2-self.offset,      -self.offset,               -self.height/2 )
            self.box.Max = XYZ(  self.width/2 + self.offset,    self.offset,  self.offset*2 )
        else:
            self.box.Max = XYZ(  self.width/2 + self.offset,     self.height + self.offset,  self.offset )  
        
        self.box.Transform = self.trans
    def details(self):     
        vue = ["plan", "elevation", "section"]
        section_type_id = doc.GetDefaultElementTypeId(ElementTypeGroup.ViewTypeSection)
        
        for i in vue:
            self.VectorTransform(i)
            self.scopeBox(i)
            view = ViewSection.CreateSection(doc, section_type_id ,self.box)
            view.Scale = 20
            curentName = "418_D_{}_{} ({})".format(self.ctg, self.name, i)
            j=0
            while True:
                try: 
                    view.Name = curentName
                    print("✅ {} {} creer avec succes".format(i, curentName))
                    break
                except:
                    curentName = curentName + " 🔎x{}".format(j)
                    j+=1

class MiseEnPage:
    
    def __init__(self,name, vues):
        self.name = name
        self.plan = vues["plan"]
        self.elevation = vues["elevation"]
        self.section = vues["section"]
        self.vues = vues

    def __repr__(self):
        return "Mise en page : \n\t- plan : {} \n\t- elevation : {} \n\t- section : {}".format(self.plan, self.elevation, self.section)
    
    def createSheet(self, i):
        with SubTransaction(doc) as St:
            sheet = ViewSheet.Create(doc, TITLEBLOCK)
            sheet.Name = self.name
            self.CreateUniqueSheetNum(sheet, i )
            if self.canAddView(sheet):
                self.addView(sheet)
                print("📄 Feuille {} creer avec succes".format(self.name))
            else:
                St.RollBack()
                print("❌ Impossible d'ajouter les vues a la feuille pour {}".format(self.name))
    
    def CreateUniqueSheetNum(self, sheet, i):
        sheetNumber = 'D418_{}'.format(i)
        while True:
            try:
                sheet.SheetNumber = sheetNumber
                break
            except:
                sheetNumber = 'D418_{}'.format(i) + "X"
    def canAddView(self, sheet):
        flag = False
        for i in self.vues:
            flag = Viewport.CanAddViewToSheet(doc, sheet.Id, self.vues[i].Id)
        return flag
    
    #TODO : créer des coordonnées dynamiques et migrée dans une boucle
    def addView(self, sheet):
        Plan = Viewport.Create(doc, sheet.Id, self.plan.Id, XYZ(0.24,0.77,0))
        elevation = Viewport.Create(doc, sheet.Id, self.elevation.Id, XYZ(0.28,0.45,0))
        section = Viewport.Create(doc, sheet.Id, self.section.Id, XYZ(0.58,0.45,0))

def getAllElement(category):
    return FilteredElementCollector(doc).OfCategory(category).WhereElementIsNotElementType().ToElements()
def FormSelector():
    ops = ["Porte", "Fenetre"]
    floorPlantype = {"Porte": BuiltInCategory.OST_Doors, "Fenetre": BuiltInCategory.OST_Windows}
    return( floorPlantype[forms.CommandSwitchWindow.show(ops, message='Selectionner le type de menuiserie')])

#TODO : ajouter la selection du type de feuille
def SheetTypeSelector():
    ops = ["A3", "A4"]
    return forms.CommandSwitchWindow.show(ops, message='Selectionner le type de feuille')


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
    with revit.Transaction(doc=pyDoc, name="detailer les elements"):
        for key, item in mainDict.items():
            try : 
                print("🔧 Detailer l'element : {}".format(key))
                Menuiserie(item).details()
            except Exception as e:
                print("❌ Erreur lors de la création des vue de details : {}".format(e))
    
    # ------------------------- mise en page des vues ------------------------- #
    allViews = [view for view in FilteredElementCollector(doc).OfClass(View).WhereElementIsNotElementType().ToElements() if view.Name.startswith("418_D")]
    dictView = defaultdict(dict)
    
    for view in allViews:
        try:
            name = view.Name.replace("418_", "").split(" (")[0]
            viewType = view.Name.split(" (")[1].split(")")[0]
            dictView[name][viewType] = view
        except Exception as e:
            print("❌ Erreur lors de la recuperation des vues : {}".format(e))
    
    with revit.Transaction(doc=pyDoc, name="Mise en page des vues"):  
        i = 0 
        for item in dictView:
            MiseEnPage(item, dictView[item]).createSheet(i)
            i+=1
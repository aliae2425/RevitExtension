# -*- coding: utf-8 -*-

# ----------------------------- pyrevit varaibles ---------------------------- #

#! python3
__title__ = 'Details menuiserie'
__doc__ = """
    version : 0.1.0
    Date : 31.03.2024
    
    crée un jeu de plan detaillant les menuiseries par type

"""
__authors__ = [
    'Aliae'
]

__min_revit_ver__ = 2024                                       
__max_revit_ver__ = 2024                                       
__highlight__ = 'new'

# -------------------------------- importation ------------------------------- #
import os
from Autodesk.Revit.DB import *  
from pyrevit import revit


# ----------------------------- global variables ----------------------------- #

activ_doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument
app = __revit__.Application


# --------------------------------- crée view -------------------------------- #

class Menuiserie:
    
    def __init__(self, name, object):
        self.object = object
        self.name = name
        self.origin = object.Location.Point
        self.host = object.Host
        self.height = object.Symbol.get_Parameter(BuiltInParameter.GENERIC_HEIGHT).AsDouble()
        self.width = object.Symbol.get_Parameter(BuiltInParameter.DOOR_WIDTH).AsDouble()
        self.offset = UnitUtils.ConvertToInternalUnits(40, UnitTypeId.Centimeters)
        
        menuiserie = []
        menuiserie["elevation"] = self.elevation()
        menuiserie["coupe"] = self.coupe()
        menuiserie["plan"] = self.plan()
        
        return menuiserie
    
    def create_scopeBox(self):
        self.vector = self.host.Location.Curve.GetEndPoint(0) - self.host.Location.Curve.GetEndPoint(1)
        self.vector = self.vector.Normalize()
        
        SectionBox = BoundingBoxXYZ()
        SectionBox.Min = XYZ(-self.width/2-self.offset, 0-self.offset, -self.offset)
        SectionBox.Max = XYZ(self.width/2+self.offset, self.height+self.offset, self.offset)

        return SectionBox

    def TransVector(self, X,Y,Z):
        trans = Transform.Identity
        trans.Origin = self.origin
        
        trans.BasisX = X
        trans.BasisY = Y
        trans.BasisZ = Z
        
        return trans

    def rename(self, view, type):
        viewName = '418_{}({})'.format(self.name, type)
        while True :
            try:
                view.Name = viewName
                print('create elevation for {}'.format(self.name))
            except:
                viewName = viewName + '-copy'
    
    def elevation(self):
        ScopeBox = self.create_scopeBox()
        ScopeBox.Transform = self.TransVector(self.origin, XYZ.BasisZ, self.vector.CrossProduct(XYZ.BasisZ))
        SectionTypeId = activ_doc.GetDefaultElementTypeId(ElementTypeGroup.ViewTypeSection)
        
        view = ViewSection.CreateSection(activ_doc, SectionTypeId, ScopeBox)
        self.rename(view, 'elevation')
    
    def coupe(self):
        ScopeBox = self.create_scopeBox()
        ScopeBox.Transform = self.TransVector(self.origin, self.vector.CrossProduct(XYZ.BasisZ), XYZ.BasisZ,  self.vector.CrossProduct(XYZ.BasisZ).CrossProduct(XYZ.BasisZ))
        SectionTypeId = activ_doc.GetDefaultElementTypeId(ElementTypeGroup.ViewTypeSection)
        
        view = ViewSection.CreateSection(activ_doc, SectionTypeId, ScopeBox)
        self.rename(view, 'coupe')
        print('create coupe for {}'.format(self.name))
              
    def plan(self):
        ScopeBox = self.create_scopeBox()
        ScopeBox.Transform = self.TransVector(self.origin, XYZ.BasisZ.CrossProduct(self.vector), XYZ.BasisZ)
        SectionTypeId = activ_doc.GetDefaultElementTypeId(ElementTypeGroup.ViewTypeSection)
        
        view = ViewSection.CreateSection(activ_doc, SectionTypeId, ScopeBox)
        self.rename(view, 'plan')
        print('create plan for {}'.format(self.name))
        
        
        
windows = FilteredElementCollector(activ_doc).OfCategory(BuiltInCategory.OST_Windows).WhereElementIsNotElementType().ToElements()

dict_windows = {}

for win in windows:
    FamilyName = win.Symbol.FamilyName
    TypeName = Element.Name.GetValue(win.Symbol)
    KeyName = '{}_{}'.format(FamilyName, TypeName)
    
    host = win.Host
    if type(host) == Wall:
        dict_windows[KeyName] = win
    else: 
        print('la fenetre {} n\'est pas dans un mur'.format(KeyName))

with revit.Transaction(doc=activ_doc, name='Details menuiserie'):
    for name, win in dict_windows.items():
        print(name)
        for view in Menuiserie(name, win):
            print(view)
        print('----------------------')

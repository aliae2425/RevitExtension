# -*- coding: utf-8 -*-
from Autodesk.Revit.DB import *

doc   = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument
app   = __revit__.Application


#recuperer les type de coupe par nom
def GetTypeByName(name, document = doc):
    items = []
    for item in FilteredElementCollector(document).OfClass(ViewFamilyType).ToElements():
        if item.Name == name:
            items.append(item)
    return items

def GetPlanbyTypeId(id, document = doc):
    items = []
    for item in FilteredElementCollector(document).OfClass(ViewPlan).ToElements():
        if item.GetTypeId() == id:
            items.append(item)
    return items
    


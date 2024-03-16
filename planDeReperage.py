from Autodesk.Revit.DB import *
from pprint import pprint
import os 

doc   = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument
app   = __revit__.Application

TYPE_PLAN_REPERAGE = 'Plan de reperage'

#recuperer les type de coupe par nom
def GetTypeByName(name):
    items = []
    for item in FilteredElementCollector(doc).OfClass(ViewFamilyType).ToElements():
        if item.Name == name:
            items.append(item)
    return items

def GetPlanbyTypeId(id):
    items = []
    for item in FilteredElementCollector(doc).OfClass(ViewPlan).ToElements():
        if item.GetTypeId() == id:
            items.append(item)
    return items
    
#recuperer les plan de type plan de reperage
type = GetTypeByName(TYPE_PLAN_REPERAGE)

if len(type) > 1:
    print("Erreur => {} type de plan de reperage trouver. 1 seul requis".format(len(type)))
else:
    print("tout vas bien")
    
sheets =  FilteredElementCollector(doc).OfClass(ViewSheet).ToElements()

t = Transaction(doc, "Rename sheets")
t.Start()
for sheet in sheets:
    print(sheet.SheetNumber)
    viewPort_id = sheet.GetAllViewports()
    for viewPort in viewPort_id:
        view = doc.GetElement(doc.GetElement(viewPort).ViewId)
        if(view.GetTypeId() == type[0].Id ):
            view.Name = "418_PDR_{}".format(sheet.SheetNumber)
            print(view.Name)

t.Commit()

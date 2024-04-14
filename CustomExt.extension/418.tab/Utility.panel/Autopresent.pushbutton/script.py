# -*- coding: utf-8 -*-

#! python3
from pyrevit import revit, forms, script
from pyrevit import DB as DB


doc = revit.doc
uidoc = revit.uidoc


class niveau: 
    def __init__(self):
        self.niveau = DB.FilteredElementCollector(doc).OfCategory(DB.BuiltInCategory.OST_Levels).WhereElementIsNotElementType().ToElements()
        self.sortLevels()
    def __repr__(self):
        for lvl in self.niveau:
            print("{} at {} | {} \n".format(lvl.Name, lvl.Elevation, lvl.ProjectElevation))
        return ""   
    def sortLevels(self):
        self.niveau = sorted(self.niveau, key=lambda x: x.Elevation)  
    def renameLevel(self):
        i = -len([lvl for lvl in self.niveau if lvl.ProjectElevation < -0.00001])
        for j, lvl in enumerate(self.niveau):
            lvl.Name = "{:02d}_R{}".format(j,i)
            i+=1
    def getLevels(self):
        return self.niveau   
        
class vue:
    def __init__(self, lvl):
        self.views = lvl.FindAssociatedPlanViewId()
        
    def createViews(self, typeId, lvl, Plan):
        vue = DB.ViewPlan.Create(doc, typeId, lvl.Id)
        vue.Name = "{}_{}".format(Plan, lvl.Name)
        # if Plan == "Projet":
        #     vue.Phas
        
    
    def getViews(self):
        return self.views

    
if __name__ == "__main__":
       
    planTravail = [PlanType for PlanType in  DB.FilteredElementCollector(doc).OfClass(DB.ViewFamilyType).ToElements()\
        if DB.Element.Name.__get__(doc.GetElement(PlanType.Id)) == "Travail"]
    if planTravail:
        print(planTravail[0].Id)
    else:
        forms.alert("Pas de type de travail trouvé.")
    
    with revit.Transaction('Rename Levels'):
        niveau().renameLevel()
    
    lvl = niveau().getLevels()
    print(lvl)
    DefaultType = doc.GetDefaultElementTypeId(DB.ElementTypeGroup.ViewTypeFloorPlan)
    with revit.Transaction('Create Views'):
        for l in lvl:
            Plan = ["Travail", "Projet", "Existant"]
            for p in Plan:
            VueTravail = DB.ViewPlan.Create(doc, planTravail[0].Id, l.Id)
            VueProjet = DB.ViewPlan.Create(doc, DefaultType, l.Id)
            VueExistant = DB.ViewPlan.Create(doc, DefaultType, l.Id)

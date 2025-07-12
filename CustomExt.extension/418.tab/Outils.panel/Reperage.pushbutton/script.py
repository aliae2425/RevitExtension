# -*- coding: utf-8 -*-

#!python3
__title__ = 'Plan de repérage'
__doc__ = """
    version : 0.1.0
    Date : 24.03.2024
    __________________
    Récupère les vues de type plan de repérage et les renomme en fonction de la feuille sur laquelle elles se trouvent ainsi que crée un filtre limitant les coupes affiché a celle dans la feuille

    __________________
    Shift-Click:

    Affiche la fenêtre de configuration pour le type de plan de repérage

"""
__authors__ = [
    'Aliae',
    'JLo'
]
__min_revit_ver__ = 2021                                    
__max_revit_ver__ = 2026                                      
__highlight__ = 'updated'
__beta__ = False


from pyrevit.userconfig import user_config
from pyrevit import script, forms
from pyrevit import DB, HOST_APP, UI, revit, script
from pyrevit.forms import alert
from pyrevit.framework import List
from re import sub

activ_document   = __revit__.ActiveUIDocument.Document
new_doc = revit.DOCS.doc
uidoc = __revit__.ActiveUIDocument
app   = __revit__.Application

# ID_TYPE_PLAN_REPERAGE = "261345"
LABEL_PLAN = "418_PDR_{}"
LABEL_FILTER = "418_PDR_S{}"

def get_floorPlan(doc):
    return DB.FilteredElementCollector(doc).OfClass(DB.ViewPlan).ToElements()

def selectFloorType(doc):
    ops = []
    floorPlantype = {}

    for section in get_floorPlan(doc):
        if section.GetTypeId() not in floorPlantype:
            if section.GetTypeId().ToString() != '-1':
                # floorPlantype[section.GetTypeId().ToString()] = DB.Element.Name.__get__(activ_document.GetElement(section.GetTypeId()))
                floorPlantype[DB.Element.Name.__get__(doc.GetElement(section.GetTypeId()))] = section.GetTypeId()

    for key, value in floorPlantype.items():
        ops.append(key)

    return( floorPlantype[forms.CommandSwitchWindow.show(ops, message='Selectionner le type plan de niveau')])

def userConfig_ID(doc):
    try:
        # check if the section exist
        user_config.add_section('localplan')
        ID_TYPE_PLAN_REPERAGE = user_config.localplan.id = int(selectFloorType(doc).ToString())
        user_config.save_changes()
        
    except:
        # look if the section exist and the id is set
        if user_config.localplan.get_option('id', "") == "":
            ID_TYPE_PLAN_REPERAGE = user_config.localplan.id = int(selectFloorType(doc).ToString())
            user_config.save_changes()
        # get the id from the config file
        else :
            ID_TYPE_PLAN_REPERAGE = user_config.localplan.get_option('id', "")
    # check if the id is still valid
    if not activ_document.GetElement(DB.ElementId(ID_TYPE_PLAN_REPERAGE)):
        ID_TYPE_PLAN_REPERAGE = user_config.localplan.id = selectFloorType(doc).ToString()
        user_config.save_changes()
        
    return ID_TYPE_PLAN_REPERAGE

def get_section(doc):
    return [section for section in DB.FilteredElementCollector(doc).OfCategory(DB.BuiltInCategory.OST_Views).ToElements() if section.ViewType.ToString() == "Section"]

def dispose_filters(doc):
    return [filter for filter in DB.FilteredElementCollector(doc).OfClass(DB.FilterElement).ToElements() if filter.Name.startswith("418_PDR_S")]

ID_TYPE_PLAN_REPERAGE = str(userConfig_ID(activ_document))

# print(ID_TYPE_PLAN_REPERAGE, type(ID_TYPE_PLAN_REPERAGE))

sheets =  DB.FilteredElementCollector(activ_document).OfClass(DB.ViewSheet).ToElements()

categories = List[DB.ElementId]()
categories.Add(DB.ElementId(DB.BuiltInCategory.OST_Sections))
param = DB.ElementId(DB.BuiltInParameter.VIEWPORT_SHEET_NUMBER)

with revit.Transaction(doc=new_doc, name="Rename sheets"):
    for sheet in sheets:
        rule = DB.ParameterFilterRuleFactory.CreateNotContainsRule(param, sheet.SheetNumber)
        viewPort_id = sheet.GetAllViewports()
        for viewPort in viewPort_id:
            view = activ_document.GetElement(activ_document.GetElement(viewPort).ViewId)
            if(view.GetTypeId().ToString() == ID_TYPE_PLAN_REPERAGE):
                view.Name = LABEL_PLAN.format(sheet.SheetNumber)
                active_filters = [filter for filter in view.GetFilters()]
                for f in active_filters:
                    current_filter = activ_document.GetElement(f).Name
                    if current_filter != LABEL_FILTER.format(sheet.SheetNumber):
                        activ_document.Delete(f)
                        print("Dans la vue {}, le filtre pour {} a été supprimé".format(view.Name, current_filter))
                try:
                    fltr = DB.ParameterFilterElement.Create(
                        activ_document, LABEL_FILTER.format(sheet.SheetNumber), categories, DB.ElementParameterFilter(rule)
                    )
                    view.AddFilter(fltr.Id)
                    view.SetFilterVisibility(fltr.Id, False)
                    print("le filtre pour la vue {} a été créé".format(view.Name))
                except:
                    print("le filtre pour la vue {} existe déjà".format(view.Name))

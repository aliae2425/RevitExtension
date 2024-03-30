# -*- coding: utf-8 -*-

#! python3

from pyrevit.userconfig import user_config
from pyrevit import script, forms
from pyrevit.forms import WPFWindow
from pyrevit import DB, HOST_APP, UI, revit, script

activ_document   = __revit__.ActiveUIDocument.Document


def get_section(doc):
    return DB.FilteredElementCollector(doc).OfClass(DB.ViewPlan).ToElements()

def selectFloorType(doc):
    ops = []
    floorPlantype = {}

    for section in get_section(doc):
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
        ID_TYPE_PLAN_REPERAGE = user_config.localplan.id = int(selectFloorType(doc).ToString())
        user_config.save_changes()
        
    return ID_TYPE_PLAN_REPERAGE


# print(userConfig_ID(activ_document))
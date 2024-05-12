# -*- coding: utf-8 -*-

#!python3
__title__ = 'Generate Wall'
__doc__ = """
    version : 0.0.0
    Date : 12.05.2024
"""
__authors__ = [
    'Aliae',
    'JLo'
]
__min_revit_ver__ = 2021                                    
__max_revit_ver__ = 2025                                      
__highlight__ = 'updated'
__beta__ = False


from pyrevit.userconfig import user_config
from pyrevit import script, forms
from pyrevit import DB, HOST_APP, UI, revit, script
from pyrevit.framework import List
from re import sub

from Autodesk.Revit.DB import *

activ_document   = __revit__.ActiveUIDocument.Document
new_doc = revit.DOCS.doc
uidoc = __revit__.ActiveUIDocument
app   = __revit__.Application




if __name__ == "__main__":
    forms.alert("Hello World")
    walltype = activ_document.GetDefaultFamilyTypeId(ElementId(BuiltInCategory.OST_Walls))
    with revit.Transaction('Create Wall'):
        wall = Wall.Create(new_doc, Line.CreateBound(XYZ(0,0,0), XYZ(0,10,0)), walltype, 0, 0, False, XYZ(0,0,1))
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

class selection :
    
    def UserSheetSelection(self):
        return forms.select_sheets(title="Selectionner les feuilles", button_name="Selectionner")

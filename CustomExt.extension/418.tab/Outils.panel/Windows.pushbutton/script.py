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
from pyrevit import Form

uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document
app = __revit__.Application



class Menuiserie:
    
    def __init__(obj):
        print(obj.Name)


def selector: 
    choice = {"portes":"OST_DOOR","fenetre":"OST_WINDOWS"}
    form - Form.Tst
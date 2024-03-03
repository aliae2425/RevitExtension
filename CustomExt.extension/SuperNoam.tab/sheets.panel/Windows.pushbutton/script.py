

__title__ = "Fenetre _ template"
__doc__ = """
    version : 0.1.1
    Date : 03/03/2024
    __________________
    un bouton pour les détaillé toutes 
"""

__author__ = 'Noam Carmi'                               
__min_revit_ver__ = 2024                                       
__max_revit_ver__ = 2024                                       
__highlight__ = 'new'    


import os, sys, datetime         
from Autodesk.Revit.DB import *  


doc   = __revit__.ActiveUIDocument.Document 
uidoc = __revit__.ActiveUIDocument          
app   = __revit__.Application               

active_view  = doc.ActiveView                   
active_level = active_view.GenLevel             
rvt_year     = int(app.VersionNumber)           
PATH_SCRIPT  = os.path.dirname(__file__)   


windows = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Windows).WhereElementIsNotElementType().ToElements()

dict_windows = {}

for win in windows:
    family_name = win.Symbol.Family.Name
    type_name = Element.Name.GetValue(win.Symbol)
    key_name = '{}_{}'.format(family_name, type_name)
    
    host = win.Host
    if type(host) == Wall:
        dict_windows[key_name] = win 
    else:
        print("l'hote de la fenetre {} ({}) n'est pas suporté".format(key_name, win.Id))

for k,v in dict_windows.items():
    print(k,v)
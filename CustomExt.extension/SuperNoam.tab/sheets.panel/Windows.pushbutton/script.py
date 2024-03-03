

__title__ = "Fenetre _ template"
__doc__ = """
    version : 0.1.1
    Date : 03.03.2024
    __________________
    un bouton pour les detailer toutes 
"""

__author__ = 'Noam Carmi'                               
__min_revit_ver__ = 2024                                       
__max_revit_ver__ = 2024                                       
__highlight__ = 'new'    

import os
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
        print("hote de la fenetre {} ({}) non suporte".format(key_name, win.Id))

# for k,v in dict_windows.items():
#     print(k,v)
    
for windows_name, window in dict_windows.items():
    win_origin = window.Location.Point #type: XYZ
    
    host_wall = window.Host
    curve = host_wall.Location.Curve
    
    pt_start = curve.GetEndPoint(0)
    pt_end = curve.GetEndPoint(1)
    
    vector = pt_end - pt_start
    
    win_height  = window.Symbol.get_Parameter(BuiltInParameter.GENERIC_HEIGHT).AsDouble()
    win_width   = window.Symbol.get_Parameter(BuiltInParameter.DOOR_WIDTH).AsDouble()
    win_depth   = UnitUtils.ConvertToInternalUnits(40, UnitTypeId.Centimeters)
    offset      = UnitUtils.ConvertToInternalUnits(40, UnitTypeId.Centimeters)
    
    print('-'*15)
    print("hauteur {}".format(win_height))
    print("largeur {}".format(win_width ))
    print("profondeur {}".format(win_depth ))
    print("offset {}".format(offset    ))
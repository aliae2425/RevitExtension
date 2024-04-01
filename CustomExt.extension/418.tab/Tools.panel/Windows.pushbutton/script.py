# -*- coding: utf-8 -*-

# ------------------------------- info pyrevit ------------------------------- #
__title__ = "Detailer les fenetres"
__doc__ = """
    version : 0.1.1
    Date : 03.03.2024
    __________________
    un bouton pour les detailer toutes 
"""
__author__ = 'Aliae'                               
__min_revit_ver__ = 2024                                       
__max_revit_ver__ = 2024                                       
__highlight__ = 'updated'    

# -------------------------------- importation ------------------------------- #

import os
from Autodesk.Revit.DB import *  
from collections import defaultdict
from pprint import pprint

# --------------------------- init variable global --------------------------- #

doc   = __revit__.ActiveUIDocument.Document 
uidoc = __revit__.ActiveUIDocument          
app   = __revit__.Application               

active_view  = doc.ActiveView                   
active_level = active_view.GenLevel             
rvt_year     = int(app.VersionNumber)           
PATH_SCRIPT  = os.path.dirname(__file__) 

titlebloc_id = doc.GetDefaultFamilyTypeId(ElementId(BuiltInCategory.OST_TitleBlocks))



# ------------------------- def fonction create View ------------------------- #
def AlreadyExist(tab, Name):
	flag = False
	viewSection = ''
	for i in tab:
		if i.Name == Name:
			flag = True
			viewSection = i
	return flag, viewSection

def createView(section_box, transform, name, type):
    section_box.Transform = transform
    
    SectionType_id = doc.GetDefaultElementTypeId(ElementTypeGroup.ViewTypeSection)
    Coupe_Types = FilteredElementCollector(doc).OfClass(ViewFamilyType).ToElements()
    # result, viewSection = AlreadyExist(Coupe_Types, "418_details")
    
    # if result : 
    #     Section = viewSection
    # else:
    #     Section = SectionType_id.Duplicate("418_Details")
    
    window_elevation = ViewSection.CreateSection(doc, SectionType_id, section_box)
    
    new_name = "418_{} ({})".format(name, type)
    
    while True:
        try:
            window_elevation.Name = new_name
            print("{} cree : {}".format(type, name))
            break
        except:
            new_name += "-copy"

def TransVector(Origin, X,Y,Z):
    trans = Transform.Identity
    trans.Origin = Origin
    
    trans.BasisX = X
    trans.BasisY = Y
    trans.BasisZ = Z
    
    return trans
    
def createElevation(origine, vector, offset, name):
    vector = vector.Normalize()

    half = win_width/2
    section_box = BoundingBoxXYZ()
    section_box.Min = XYZ(-half-offset, 0-offset, -offset)
    section_box.Max = XYZ(half + offset, win_height+offset, offset)

    trans = TransVector(origine, vector, XYZ.BasisZ, vector.CrossProduct(XYZ.BasisZ))

    createView(section_box, trans, name, "elevation")
   
def createCrossSection(origine, vector, offset , name):
    vector = vector.Normalize()
    
    half = win_width/2
    section_box = BoundingBoxXYZ()
    section_box.Min = XYZ(-half-offset, 0-offset, -offset)
    section_box.Max = XYZ(half + offset, win_height+offset, offset)

    vector_cross = vector.CrossProduct(XYZ.BasisZ)
    trans = TransVector(origine, vector_cross, XYZ.BasisZ, vector_cross.CrossProduct(XYZ.BasisZ))
    
    createView(section_box, trans, name, "coupe")

def createPlan(origine, vector, offset, name):
    vector = vector.Normalize()

    trans = TransVector(origine, vector, XYZ.BasisZ.CrossProduct(vector), XYZ.BasisZ)

    half = win_width/2
    section_box = BoundingBoxXYZ()
    section_box.Min = XYZ(-half-offset, 0-offset, offset)
    section_box.Max = XYZ(half + offset, win_height+offset, offset*2)

    createView(section_box, trans, name, "plan")
    
def createViewOfType(origine, vector, offset, name, type):
    vector = vector.Normalize()

    half = win_width/2
    section_box = BoundingBoxXYZ()
    section_box.Min = XYZ(-half-offset, 0-offset, -offset)
    section_box.Max = XYZ(half + offset, win_height+offset, offset)

    if type == "elevation":
        trans = TransVector(origine, vector, XYZ.BasisZ, vector.CrossProduct(XYZ.BasisZ))
    elif type == "plan":
        trans = TransVector(origine, vector, XYZ.BasisZ.CrossProduct(vector), XYZ.BasisZ)
    elif type == "coupe":
        vector_cross = vector.CrossProduct(XYZ.BasisZ)
        trans = TransVector(origine, vector_cross, XYZ.BasisZ, vector_cross.CrossProduct(XYZ.BasisZ))
    else:
        raise ValueError("Invalid view type")

    createView(section_box, trans, name, type)


# ------------------------- def function create sheet ------------------------ #

def MiseEnPage():
    all_views = FilteredElementCollector(doc).OfClass(View).WhereElementIsNotElementType().ToElements()
    view_to_use = [view for view in all_views if "418" in view.Name]

    dict_views = defaultdict(dict)
    
    for view in view_to_use:
        try:
            view_name = view.Name.replace('418_','').split(' (')[0]
            
            curent = ''
            for idx in range(view.Name.index('(')-1 + len('(') + 1, view.Name.index(")")):
                curent = curent + view.Name[idx]
            
            dict_views[view_name][curent] = view
            
        except:
            pass
    
    i=0
    for win_name, dict_win_views in dict_views.items():
        createsheet(win_name, dict_win_views, i)
        print("{} _ {}".format(win_name, dict_win_views))
        i+=1
        
        
def createsheet(win_name, dict_win_views, ite):
    new_sheet = ViewSheet.Create(doc, titlebloc_id)
   
    pt_plan = XYZ(0.5,.35,0)
    pt_Cross = XYZ(0.25,0.35,0)
    pt_Elev = XYZ(0.5,0.46,0)

    st = SubTransaction(doc)
    st.Start
    
    if Viewport.CanAddViewToSheet(doc, new_sheet.Id, dict_win_views["plan"].Id) and \
        Viewport.CanAddViewToSheet(doc, new_sheet.Id, dict_win_views["coupe"].Id) and \
        Viewport.CanAddViewToSheet(doc, new_sheet.Id, dict_win_views["elevation"].Id) :
                                  
            # vp_plan = Viewport.Create(doc, new_sheet.Id, dict_win_views["plan"].Id, pt_plan)
            # vp_plan = Viewport.Create(doc, new_sheet.Id, dict_win_views["coupe"].Id, pt_Cross)
            # vp_plan = Viewport.Create(doc, new_sheet.Id, dict_win_views["elevation"].Id, pt_Elev)
            
            print("feuille pour {} cree".format(win_name))
            
            try:
                new_sheet.SheetNumber = "418_detail_{}".format(ite)
                new_sheet.Name = '{}'.format(win_name)
            except: 
                pass
            
            st.Commit()
    else:
        st.RollBack()
        print("erreur : {} deja presente dans une feuille ".format(win_name))
        
# ----------------------------------- main ----------------------------------- #

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

t = Transaction(doc, "Generation des vues")

t.Start()

for windows_name, window in dict_windows.items():
    try: 
        win_origin = window.Location.Point 
        host_wall = window.Host
        curve = host_wall.Location.Curve
        
        vector = curve.GetEndPoint(0) - curve.GetEndPoint(1)
        
        win_height  = window.Symbol.get_Parameter(BuiltInParameter.GENERIC_HEIGHT).AsDouble()
        win_width   = window.Symbol.get_Parameter(BuiltInParameter.DOOR_WIDTH).AsDouble()
        offset = win_depth = UnitUtils.ConvertToInternalUnits(40, UnitTypeId.Centimeters)
        if not win_height:
            win_height = window.Symbol.LookupParameter('FAMILY_ROUGH_HEIGHT_PARAM').AsDouble()
        
        print("-"*25)
        
        createViewOfType(win_origin, vector, offset, windows_name, "elevation")
        createViewOfType(win_origin, vector, offset, windows_name, "plan")
        createViewOfType(win_origin, vector, offset, windows_name, "coupe")
        
        # createElevation(win_origin,vector, offset, windows_name)
        # createCrossSection(win_origin,vector,win_width/2,windows_name)
        # createPlan(win_origin,vector,win_width/2,windows_name)
        
    except:
        import traceback
        print("-"*15)
        print("Oups erreur : ")
        print(traceback.format_exc())    
    
print("# ----------------------------- getview ----------------------------- #")
MiseEnPage()

t.Commit()
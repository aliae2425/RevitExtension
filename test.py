import os
from Autodesk.Revit.DB import *

doc   = __revit__.ActiveUIDocument.Document 
uidoc = __revit__.ActiveUIDocument          
app   = __revit__.Application      

def AlreadyExist(tab, Name):
	flag = False
	viewSection = ''
	for i in tab:
		if i.Name == Name:
			flag = True
			viewSection = i
	return flag, viewSection

SectionType_id = doc.GetElement(doc.GetDefaultElementTypeId(ElementTypeGroup.ViewTypeSection))
Coupe_Types = viewFamilyTypes = FilteredElementCollector(doc).OfClass(ViewFamilyType).ToElements()

result, viewSection = AlreadyExist(Coupe_Types, "418_details")


t = Transaction(doc, "Add views")
t.Start()

if result : 
	Section = viewSection
else:
	Section = SectionType_id.Duplicate("418_Details")
 
print(Section.id)


t.Commit()
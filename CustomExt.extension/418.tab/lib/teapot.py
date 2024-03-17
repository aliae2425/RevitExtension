import json
from Autodesk.Revit.DB import *
from pyrevit import DB

doc   = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument
app   = __revit__.Application

STORAGE = "418.json"

class Statement():
    
    def __init__(self):
        with open(STORAGE, "r") as f:
            params = json.load(f)
        self.ID_TYPE_PLAN_REPERAGE = params["ID_TYPE_PLAN_REPERAGE"]
        self.COMPANY_NAME = params["COMPANY_NAME"]

    def printStatement(self):
        print("ID_TYPE_PLAN_REPERAGE: {}".format(self.ID_TYPE_PLAN_REPERAGE))
        print("COMPANY_NAME: {}".format(self.COMPANY_NAME))
    
    def editStatement(self, new_params):
        with open(STORAGE, "w") as f:
            json.dump(new_params, f)
            
    def changeCompanyName(self, new_name):
        new_params = {
            "COMPANY_NAME": new_name
        }
        self.editStatement(new_params)
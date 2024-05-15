import sqlite3,os,io,clr
from dataclasses import dataclass
from pyrevit.userconfig import user_config
from pyrevit.forms import WPFWindow
from pyrevit import DB, HOST_APP, UI, revit, script, forms, framework

activ_document   = __revit__.ActiveUIDocument.Document

def init_database(filename):
    with open("database.sql", 'r') as f:
        sql = f.read()
    con = sqlite3.connect(filename)
    cur = con.cursor()
    cur.executescript(sql)
    con.commit()
    con.close()

def get_structure():
    PROJECT_PATH = os.path.normpath(os.path.join(__file__, '../../../../'))
    EXTENSION_PATH = os.path.join(PROJECT_PATH, 'CustomExt.extension')
    print(os.listdir(EXTENSION_PATH))
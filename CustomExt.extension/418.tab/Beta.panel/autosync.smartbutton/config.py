from pyrevit.userconfig import user_config
from pyrevit import DB, forms
import time

activ_document   = __revit__.ActiveUIDocument.Document

timer = {
    '5min': 300,
    '15min': 900,
    '1/2h': 1800,
    '45m': 2700,
    '1h': 3600
}

def timerForm():
    ops = ['5min', '15min', '1/2h', '45m', '1h']
    return( timer[forms.CommandSwitchWindow.show(ops, message='Selectionner le type plan de niveau')])

def userConfig_ID():
    try:
        # check if the section exist
        user_config.add_section('autoSync')
        user_config.autoSync.time = timerForm()
        user_config.save_changes()
        # print("config created")
    except:
        user_config.autoSync.time = timerForm()
        user_config.save_changes()
        # print("config saved _ {}".format(user_config.autoSync.time))

if __name__ == "__main__":
    userConfig_ID()
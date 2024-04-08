# -*- coding: utf-8 -*-
#! python3
"""Keep views synchronized. This means that as you pan and zoom and
switch between Plan and RCP views, this tool will keep the views
in the same zoomed area so you can keep working in the same
area without the need to zoom and pan again.
This tool works best when the views are maximized.
"""
#pylint: disable=import-error,invalid-name,broad-except,superfluous-parens
import datetime

from pyrevit import EXEC_PARAMS
from pyrevit import framework
from pyrevit import DB, coreutils
from pyrevit import UI, revit, HOST_APP
from pyrevit import script, forms
from pyrevit.userconfig import user_config

doc = revit.doc
logger = script.get_logger()

AUTO_SYNC_ENV_VAR = 'AUTOSYNCACTIVE'
LAST_SYNC = 'DateTime_last_sync'

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

def userConfigTimer():
    try:
        # check if the section exist
        user_config.add_section('autoSync')
        TIMER = user_config.autoSync.time = timerForm(doc)
        user_config.save_changes()
    except:
        # look if the section exist and the id is set
        if user_config.autoSync.get_option('time', "") == "":
            TIMER = user_config.autoSync.time = timerForm(doc)
            user_config.save_changes()
        # get the id from the config file
        else :
            TIMER = user_config.autoSync.get_option('time', "")
        
    return TIMER


def toggle_state():
    """Toggle tool state"""
    new_state = not script.get_envvar(AUTO_SYNC_ENV_VAR)
    logger.info("new_state : {}".format(new_state))
    # remove last datafile on start
    script.set_envvar(AUTO_SYNC_ENV_VAR, new_state)
    # script.set_envvar(LAST_SYNC, datetime.datetime.now())
    script.toggle_icon(new_state)

def echo(sender, args):
    """Echo tool state"""
    try :
        timer = script.get_envvar(LAST_SYNC)
        duration = datetime.datetime.now() - timer
        logger.info(duration.total_seconds())
    except Exception as e:
        logger.info(e)
    

def __selfinit__(script_cmp, ui_button_cmp, __rvt__):
    """pyRevit smartbuttom init"""
    script.set_envvar(LAST_SYNC, datetime.datetime.now())
    logger.info("init at : {}".format(datetime.datetime.now()))
    logger.info("-"*25)
    try:
        __rvt__.ViewActivating += \
            framework.EventHandler[
                UI.Events.ViewActivatingEventArgs](echo)
        __rvt__.ViewActivated += \
            framework.EventHandler[
                UI.Events.ViewActivatedEventArgs](echo)
        return True
    except Exception:
        logger.info("Failed to initialize the tool.")



if __name__ == '__main__':
    toggle_state()

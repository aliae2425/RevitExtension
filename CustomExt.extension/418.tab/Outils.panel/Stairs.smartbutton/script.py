# -*- coding: utf-8 -*-

__title__ = "Echappée"
__doc__ = """
    version : 0.0.1
    Date : 10.04.2024
    __________________
    crée un volume pour l'échappée de l'escalier selectionné
"""
__author__ = 'Aliae'                               
__min_revit_ver__ = 2024                                       
__max_revit_ver__ = 2025

def __selfinit__(script_cmp, ui_button_cmp, __rvt__):
    print("hello world ")
    
    
from pyrevit import EXEC_PARAMS
from pyrevit import framework
from pyrevit import DB, coreutils
from pyrevit import UI, revit, HOST_APP
from pyrevit import script, forms
from pyrevit.userconfig import user_config

doc = revit.doc
logger = script.get_logger()

AUTO_SYNC_ENV_VAR = 'ENABLE_STAIRS_AUTO_SYNC'

def toggle_state():
    """Toggle tool state"""
    new_state = not script.get_envvar(AUTO_SYNC_ENV_VAR)
    logger.info("new_state : {}".format(new_state))
    # remove last datafile on start
    script.set_envvar(AUTO_SYNC_ENV_VAR, new_state)
    script.toggle_icon(new_state)


if __name__ == '__main__':
    toggle_state()
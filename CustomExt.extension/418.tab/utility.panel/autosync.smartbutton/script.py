"""Keep views synchronized. This means that as you pan and zoom and
switch between Plan and RCP views, this tool will keep the views
in the same zoomed area so you can keep working in the same
area without the need to zoom and pan again.
This tool works best when the views are maximized.
"""
#pylint: disable=import-error,invalid-name,broad-except,superfluous-parens
import os
import os.path as op
import pickle as pl
import math

from pyrevit import framework
from pyrevit import script, revit
from pyrevit import DB, UI


logger = script.get_logger()


SYNC_VIEW_ENV_VAR = 'SYNCVIEWACTIVE'

SUPPORTED_VIEW_TYPES = (
    DB.ViewPlan,
    DB.ViewSection,
    DB.View3D,
    DB.ViewSheet,
    DB.ViewDrafting
)


def toggle_state():
    """Toggle tool state"""
    new_state = not script.get_envvar(SYNC_VIEW_ENV_VAR)
    # remove last datafile on start
    if new_state:
        # try:
        if os.path.exists(data_filename):
            os.remove(data_filename)
        # except Exception:
        #     pass
    script.set_envvar(SYNC_VIEW_ENV_VAR, new_state)
    script.toggle_icon(new_state)


#pylint: disable=unused-argument
def __selfinit__(script_cmp, ui_button_cmp, __rvt__):
    """pyRevit smartbuttom init"""
    try:
        logger.dev_log("coucou")
        return True
    except Exception:
        return False


if __name__ == '__main__':
    toggle_state()

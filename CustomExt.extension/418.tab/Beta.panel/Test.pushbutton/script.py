# -*- coding: utf-8 -*-
__author__ = 'Aliae'                               
__min_revit_ver__ = 2024                                       
__max_revit_ver__ = 2024                                       
__highlight__ = 'updated'  
_logusage__ = True

import datetime

from pyrevit import EXEC_PARAMS
from pyrevit import framework
from pyrevit import DB, coreutils
from pyrevit import UI, revit, HOST_APP
from pyrevit import script, forms
from pyrevit.userconfig import user_config

doc = revit.doc
logger = script.get_logger()

logger.info("Hello from Beta panel!")
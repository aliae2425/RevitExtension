# -*- coding: utf-8 -*-


from pyrevit import revit, forms, script
from pyrevit import DB as DB

import clr
import wpf
clr.AddReference('System.Windows.Forms')
clr.AddReference('IronPython.Wpf')
from System import Windows

class Myform(Windows.Window):
    def __init__(self, fileName):
        wpf.LoadComponent(self, script.get_bundle_file(fileName))

Myform('AutoPresent.xaml').ShowDialog()
# -*- coding: utf-8 -*-

#! python3
from System import Windows
from pyrevit.userconfig import user_config
from pyrevit.forms import WPFWindow
from pyrevit import DB, HOST_APP, UI, revit, script, forms, framework
import os 
import sqlite3
from dataclasses import dataclass

activ_document   = __revit__.ActiveUIDocument.Document

import clr
import wpf
clr.AddReference('System.Windows.Forms')
clr.AddReference('IronPython.Wpf')


class Myform(framework.Windows.Window):

    def set_image_source(self, wpf_element, image_file):
        """Set source file for image element.

        Args:
            wpf_element (System.Windows.Controls.Image): xaml image element
            image_file (str): image file path
        """
        WPFWindow.set_image_source_file(wpf_element, image_file)
        
    def __init__(self, fileName):
        wpf.LoadComponent(self, script.get_bundle_file(fileName))
        self.set_image_source(self.logo, 'Logo.png')
        
    def abort(self, sender, e):
        self.Close()

   

# Myform('Browser.xaml').ShowDialog()
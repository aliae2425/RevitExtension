# -*- coding: utf-8 -*-

import os
import clr

from pyrevit.userconfig import user_config
from pyrevit.forms import WPFWindow
from pyrevit import DB, HOST_APP, UI, revit, script, forms, framework


activ_document   = __revit__.ActiveUIDocument.Document

import wpf
clr.AddReference('System.Windows.Forms')
clr.AddReference('IronPython.Wpf')

class T_settings(forms.WPFWindow):

    def set_image_source(self, wpf_element, image_file):
        """Set source file for image element.

        Args:
            wpf_element (System.Windows.Controls.Image): xaml image element
            image_file (str): image file path
        """
        WPFWindow.set_image_source_file(wpf_element, image_file)
        
    def __init__(self, fileName):
        wpf.LoadComponent(self, script.get_bundle_file(fileName))
        self.set_image_source(self.logo, 'Settings.png')
        self.libfile_tb = {}
        self.libfile_tb.path = user_config.get_option('libBrowser', 'libfile', '')
        
    def pick_tlib_folder(self, sender, args):
        """Callback method for picking destination folder for telemetry files"""
        new_path = forms.pick_folder(owner=self)
        if new_path:
            self.libfile_tb.path = os.path.normpath(new_path)

T_settings('Settings.xaml').ShowDialog()
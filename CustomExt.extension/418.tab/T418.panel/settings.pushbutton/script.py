# -*- coding: utf-8 -*-

import os,io
import clr
import json
import subprocess

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
        try:
            self.libfile_path.Text = user_config.libfile.get_option('path', '')
        except:
            self.libfile_path.Text = ''
            
    def pick_libfile_path(self, sender, args):
        """Callback method for picking destination folder for telemetry files"""
        new_path = forms.pick_folder(owner=self)
        if new_path:
            self.libfile_path.Text = os.path.normpath(new_path)
        self.save_settings()
        self.compute_libfile_path()
    
    def reset_libfile_path(self, sender, args):
        self.libfile_path.Text = ''
        self.save_settings()
    
    def compute_libfile_path(self):
        # print('compute_libfile_path')
        if not self.libfile_path.Text:
            forms.alert('Please select a folder for the library file.', exitscript=True)
        else : 
            path = os.path.join(self.libfile_path.Text, 'libfile.json')
            if os.path.exists(path):
                with io.open(path, 'w', encoding='utf8') as f:
                    json.dump(self.path_to_dict(path=self.libfile_path.Text), f, ensure_ascii=False)

        
    def path_to_dict(self, path):
        d = {'name': os.path.basename(path)}
        if os.path.isdir(path):
            d['type'] = "directory"
            d['children'] = [self.path_to_dict(os.path.join(path,x)) for x in os.listdir(path)]
        else:
            d['type'] = "file"
        return d
    
    def save_settings(self):
        try :
            user_config.add_section('libfile')
        except Exception as e:
            pass      
        try:
            user_config.libfile.path = self.libfile_path.Text
            user_config.save_changes()
        except Exception as e:
            forms.alert('Error saving settings: {}'.format(e), exitscript=True)
            
    def close_settings(self, sender, args):
        self.Close()

T_settings('Settings.xaml').ShowDialog()
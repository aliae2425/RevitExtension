# -*- coding: utf-8 -*-

#! python3
from pyrevit.userconfig import user_config
from pyrevit.forms import WPFWindow
from pyrevit import DB, HOST_APP, UI, revit, script, forms, framework
import os 
import json

activ_document   = __revit__.ActiveUIDocument.Document


# -*- coding: utf-8 -*-


from pyrevit import revit, forms, script
from pyrevit import DB as DB

import clr
import wpf
clr.AddReference('System.Windows.Forms')
clr.AddReference('IronPython.Wpf')
from System import Windows


class librairie(forms.Reactive):
    
    def __init__(self):
        self.directorys = folder("root")
        path_folder = user_config.libfile.get_option('path', '')
        path_file = os.path.join(path_folder, 'libfile.json')
        with open(path_file) as f:
            data = json.load(f)
        self.init_data(data, self.directorys)
        print(len(data["children"]))
        print(len(self.directorys.child))
        print(len(self.directorys.item))
        print(self.directorys)

    def init_data(self, data, current, row = 0):
            if data["type"] == "directory":
                print("{}📂 -{}- : {}".format("_"*row, current.title, data["name"]))
                fold = folder(data["name"])
                for i in data["children"]:
                    current.child.append(self.init_data(i, fold, row + 1))
            else:
                if data["name"].endswith(".rfa"):
                    print("{}📄 -{}- : {}".format("_"*row, current.title, data["name"]))    
                    familly = item(data["name"])
                    current.item.append(familly)


    
class folder(forms.Reactive):
        
        def __init__(self, title = "folder"):
            self.title = title
            self.child = []
            self.item = []
        
        def __repr__(self):
            return "📂 {} : \n _ {} sous dossiers \n _ {} fichier".format(self.title, len(self.child), len(self.item))
        
        @forms.reactive
        def title(self):
            return self._title
        
        @title.setter
        def title(self, value):
            self._title = value

class item(forms.Reactive): 
        
        def __init__(self, name = "item"):
            self.title =  name
        
        @forms.reactive
        def title(self):
            return self._title
        
        @title.setter
        def title(self, value):
            self._title = value

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
        self.folderlist = librairie()
        
    def abort(self, sender, e):
        self.Close()

   

lib = librairie()
# Myform('Browser.xaml').ShowDialog()
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


class folder(forms.Reactive):
        
        def __init__(self, title = "folder", child = [], item = []):
            self.title = title
            self.child = child
            self.item = item
        
        # def __repr__(self):
        #     return "📂 {} : _ {} sous dossiers, _ {} fichier"\
        #         .format(self.title, len(self.child), len(self.item))
        
        def get_child(self):
            return self.child
        
        def get_item(self):
            return self.item
        
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


class librairie(forms.Reactive):
    
    def __init__(self):
        self.directorys = folder("root")
        path_folder = user_config.libfile.get_option('path', '')
        path_file = os.path.join(path_folder, 'libfile.json')
        with open(path_file) as f:
            data = json.load(f)
        for i in data["children"]:
            self.init_data(i, self.directorys)
        return self.directorys

    def init_data(self, data, current, row = 0):
        print("~~~~ folder : {} ~~~~ child : {} / item : {}".format(current.title, len(current.child), len(current.item)))
        if data["type"] == "directory":
            print("{}📂: {}".format("-"*row, data["name"]))
            fold = folder(title=data["name"])
            fold.child = [self.init_data(x, fold, row+1) for x in data["children"]]
            current.child.append(fold)
            return fold
        else:
            if data["name"].endswith(".rfa"):
                print("{}📄: {}".format("-"*row, data["name"]))    
                familly = item(data["name"])
                current.item.append(familly)
        print("//// folder : {} ~~~~ child : {} / item : {}".format(current.title, len(current.child), len(current.item)))


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

   

lib = librairie().directorys
print("lib : {}".format(lib))
for i in lib.get_child():
    print(i.title)
    # for j in i.get_child():
    #     print(j)
    #     for k in j.get_item():
    #         print(k)
# Myform('Browser.xaml').ShowDialog()
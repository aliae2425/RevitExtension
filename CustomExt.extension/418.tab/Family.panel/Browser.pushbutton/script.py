# -*- coding: utf-8 -*-

#! python3
from pyrevit.userconfig import user_config
from pyrevit.forms import WPFWindow
from pyrevit import DB, HOST_APP, UI, revit, script, forms, framework


activ_document   = __revit__.ActiveUIDocument.Document


# -*- coding: utf-8 -*-


from pyrevit import revit, forms, script
from pyrevit import DB as DB

import clr
import wpf
clr.AddReference('System.Windows.Forms')
clr.AddReference('IronPython.Wpf')
from System import Windows


test = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]
Folder = { 1 :{"Porte" : {"simple", "double", "sous tenture", "tierse"}}\
    ,2 : {"Mobilier": {"table", "chaise", "armoire", "lit"}}\
    ,3:{ "Fenetre"}, 4:{"Plante"}\
    ,5:{"Luminaire" : {"plafonnier", "applique", "suspension", "lampe de bureau"}}\
    ,6:{ "Sanitaire" : {"lavabo", "wc", "douche", "baignoire"}}
    }

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
        self.FolderItem = test
        
        haha = Folder[1]
        # self.set_image_source(self.placeholder, 'UserControl/image.png')
        # self.set_image_source(self.placeholder1, 'UserControl/image.png')
        # self.set_image_source(self.placeholder2, 'UserControl/image.png')
        # self.set_image_source(self.placeholder3, 'UserControl/image.png')
        # self.set_image_source(self.placeholder4, 'UserControl/image.png')
        # self.set_image_source(self.placeholder5, 'UserControl/image.png')
        # self.set_image_source(self.placeholder6, 'UserControl/image.png')
        # self.set_image_source(self.placeholder7, 'UserControl/image.png')
        # self.set_image_source(self.placeholder8, 'UserControl/image.png')
        # self.set_image_source(self.placeholder9, 'UserControl/image.png')
        # self.set_image_source(self.placeholder10, 'UserControl/image.png')
        # self.set_image_source(self.placeholder11, 'UserControl/image.png')
        # self.set_image_source(self.placeholder12, 'UserControl/image.png')
        # self.set_image_source(self.placeholder13, 'UserControl/image.png')
        # self.set_image_source(self.placeholder14, 'UserControl/image.png')
        # self.set_image_source(self.placeholder15, 'UserControl/image.png')
        
    def abort(self, sender, e):
        self.Close()

   

Myform('Browser.xaml').ShowDialog()
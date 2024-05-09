# -*- coding: utf-8 -*-

import os,io,json

from pyrevit.userconfig import user_config
from pyrevit import DB, HOST_APP, UI, revit, script, forms, framework


activ_document   = __revit__.ActiveUIDocument.Document

class T_settings():
        
    def __init__(self):
        try:
            self.libfile_path = user_config.libfile.get_option('path', '')
        except:
            forms.alert('Please select a folder for the library file.', exitscript=True)
        self.compute_libfile_path()
        
            
    def compute_libfile_path(self):
        # print('compute_libfile_path')
        if not self.libfile_path:
            forms.alert('Please select a folder for the library file.', exitscript=True)
        else : 
            path = os.path.join(self.libfile_path, 'libfile.json')
            with io.open(path, 'w', encoding='utf8') as f:
                json.dump(self.path_to_dict(path=self.libfile_path), f, ensure_ascii=False)
            forms.alert('The library file has been force update.', exitscript=True)

        
    def path_to_dict(self, path):
        d = {'name': os.path.basename(path)}
        if os.path.isdir(path):
            d['type'] = "directory"
            d['children'] = [self.path_to_dict(os.path.join(path,x)) for x in os.listdir(path)]
        else:
            d['type'] = "file"
        return d


if __name__ == "__main__":
    T_settings()

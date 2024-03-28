# -*- coding: utf-8 -*-

#! python3
from pyrevit import forms

from pyrevit import script
from pyrevit.userconfig import user_config

try :
    user_config.add_section('newsection')
    user_config.newsection.property = 'test2'
except:
    user_config.newsection.property = 'test4'
user_config.save_changes()

print(dir(user_config))

print(user_config.newsection.get_option('property', "default_value"))


# ops = ['option1', 'option2', 'option3', 'option4']
# forms.CommandSwitchWindow.show(ops, message='Select Option')

# ops = ['option1', 'option2', 'option3', 'option4']
# switches = ['switch1', 'switch2']
# cfgs = {'option1': { 'background': '0xFF55FF'}}
# rops, rswitches = forms.CommandSwitchWindow.show(ops,switches=switches,message='Select Option',config=cfgs,recognize_access_key=False)
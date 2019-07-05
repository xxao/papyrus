#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

# import modules
import os.path
import json

VERSION = (2,0,0)
CONFIG_PATH = './papyrus.json'

_PARAMS = dict(
    
    # value, func, store
    
    # path to the library DB to open at start
    library = ['', str, True],
    recent_days = [10, int, True],
    
    # application layout
    unlock_ui = [False, bool, False],
    menu_bar_enabled = [True, bool, True],
    app_maximized = [False, bool, True],
    app_width = [1500, int, True],
    app_height = [800, int, True],
    
    # collections view
    collections_view_enabled = [True, bool, True],
    collections_view_width = [220, int, True],
    
    # PDF view
    pdf_view_enabled = [False, bool, True],
    pdf_view_height = [300, int, True],
    
    # details view
    details_view_enabled = [True, bool, True],
    details_view_width = [270, int, True],
    
    # automatic (re)moving of PDF cover page
    # mode: 1-delete, 2-move to end
    cover_remove_mode = [None, int, True],
    cover_remove_tag = [None, str, True]
)

# init default settings
SETTINGS = dict()


def load(path=CONFIG_PATH):
    """Loads settings from existing config file."""
    
    # init defaults
    for param, val in _PARAMS.items():
        
        value, func, store = val
        if value is not None:
            value = func(value)
        
        SETTINGS[param] = value
    
    # check path
    if not os.path.exists(path):
        return False
    
    # load settings
    try:
        
        # load data
        with open(path, 'r') as f:
            data = json.load(f)
        
        # get params
        params = list(SETTINGS.keys())
        
        # parse settings
        for param in params:
            
            # get value
            value = data.get(param, None)
            if value is None:
                continue
            
            # set converted value
            try:
                SETTINGS[param] = _PARAMS[param][1](value)
            except ValueError:
                continue
            
            # mark to save
            _PARAMS[param][2] = True
        
        return True
    
    except:
        return False


def save(path=CONFIG_PATH):
    """Saves current settings to config file."""
    
    # get params to save
    settings = {k:v for k,v in SETTINGS.items() if _PARAMS[k][2]}
    
    # save settings
    try:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(json.dumps(settings, indent=4))
        return True
    
    except:
        return False

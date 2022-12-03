setting = {
    'filepath' : __file__,
    'use_db': True,
    'use_default_setting': True,
    'home_module': None,
    'menu': None,
    'setting_menu': None,
    'setting_menu': {
        'uri': f"trans/base/setting",
        'name': '번역 설정',
    },
    'default_route': 'normal',
}

from plugin import *

P = create_plugin_instance(setting)

from .mod_base import ModuleBase

P.set_module_list([ModuleBase])


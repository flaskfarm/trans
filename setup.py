__menu = {
    'uri': __package__,
    'name': '번역',
    'list': [
        {
            'uri': 'base',
            'name': '설정',
        },
        {
            'uri': 'manual',
            'name': '매뉴얼',
            'list': [
                {
                    'uri': 'README.md',
                    'name': 'README'
                }
            ]
        },
        {
            'uri': 'log',
            'name': '로그',
        },
    ]
}


setting = {
    'filepath' : __file__,
    'use_db': True,
    'use_default_setting': True,
    'home_module': None,
    'menu': __menu,
    'setting_menu': None,
    'default_route': 'normal',
}

from plugin import *

P = create_plugin_instance(setting)

from .mod_base import ModuleBase

P.set_module_list([ModuleBase])


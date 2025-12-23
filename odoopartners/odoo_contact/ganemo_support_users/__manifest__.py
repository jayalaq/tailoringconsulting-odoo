# -*- coding: utf-8 -*-
{
    'name': "Ganemo Premium Odoo Support Request",
    "version": "17.0.0.0.1",
    "category": "Productivity ",
    "summary": "Create Odoo Support Request To Ganemo using whatsapp",
    "description": """ It helps you create support tickets to Ganemo from your own Odoo using whatsapp.""",
    'author': 'Ganemo',
    'company': 'Ganemo SAC',
    'maintainer': 'Ganemo',
    'website': "https://www.ganemo.co",
    'depends': ['base', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'wizard/client_support_views.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'ganemo_support_users/static/src/js/systray_icons.js',
            'ganemo_support_users/static/src/xml/systray_icon.xml',
            'ganemo_support_users/static/src/css/client_support.css',
            'https://cdn.jsdelivr.net/npm/remixicon/fonts/remixicon.css',
        ]
    },
    'images': ['static/description/banner.jpg'],
    'license': 'LGPL-3',
    'installable': True,
    'auto_install': False,
    'application': False,
    'price': 20.00,
    'module_type': 'official',
}

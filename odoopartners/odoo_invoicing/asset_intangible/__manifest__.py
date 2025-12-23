{
    'name': 'Relate depreciation and amortization of an asset',
    'version': '17.0.1.0.1',
    'author': 'Ganemo',
    'website': 'https://www.ganemo.co',
    'category': 'Accounting',
    'summary': 'Asset Depreciation Linker Module',
    'description': """
This module will serve us to link the depreciation or amortization of an asset.
""",
    'depends': [
        'account'
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/asset_intangible_menus.xml',
        'views/asset_intangible_views.xml',
        'views/account_move_views.xml',
        'views/account_move_line_views.xml'        
    ],
    'application': False,
    'installable': True,
    'auto_install': False,
    'license': 'Other proprietary',
    'currency': 'USD',
    'price': 10.00,
    'module_type': 'official'
}

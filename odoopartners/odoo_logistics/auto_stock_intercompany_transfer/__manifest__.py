{
    'name': 'Auto Inter Company Stock Transfer',
    'version': '17.0.1.1.2',
    'category': 'Inventory',
    'summary': """Auto Create counterpart Receipt/Delivery Orders between
     Odoo companies.""",
    'description': """Automates the creation of receipt/delivery orders
     between companies when validating inventory transfers.""",
    'author': 'Ganemo',
    'company': 'Ganemo',
    'website': "https://www.ganemo.co",
    'depends': ['stock', 'account'],
    'data': [
        'views/res_company_views.xml',
    ],
    'images': ['static/description/banner.png'],
    'license': 'Other proprietary',
    'installable': True,
    'auto_install': False,
    'application': False,
    'currency': 'USD',
    'price': 97.0,
    'module_type': 'official'
}

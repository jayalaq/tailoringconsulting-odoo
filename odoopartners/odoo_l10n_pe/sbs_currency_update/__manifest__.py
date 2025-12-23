{
    'name': 'SBS - Currency Update',
    'version': '17.0.1.1.0',
    'author': 'Ganemo',
    'website': 'https://www.ganemo.co',
    'category': 'Accounting',
    'summary': 'Register in the rates of the Currency dollars of Odoo; the sale exchange rate according to SUNAT.',
    'description':""" 
This module will allow us to create a planned action that we will find in the "settings/technical/planned actions" path. It will also store the USD currency exchange rate so it can be used on invoices.
""",
    'depends': [
        'account',
        'api_data_token'
    ],
    'data': [
        'data/ir_cron.xml'
    ],
    'application':False,
    'installable': True,
    'auto_install': False,
    'license': 'Other proprietary',
    'currency': 'USD',
    'price': 0.00,
    'module_type': 'official',
}

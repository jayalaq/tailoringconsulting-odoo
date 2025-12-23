{
    'name': 'To break restriction exchange rates on the same day',
    'version': '17.0.1.0.0',
    'author': "Ganemo",
    'website': "https://www.ganemo.co",
    'category': 'Accounting',
    'summary': "This module will allow us to place 2 exchange rates on the same day",
    'description': """
This module will allow us to place 2 exchange rates on the same day.
""",
    'depends': [
        'account'
    ],
    'data': [
        'data/no_res_currency_rate.xml'
    ],
    'post_init_hook': 'post_init_hook',
    'license': 'Other proprietary',
    'price': 0.00,
    'module_type': 'official',
}

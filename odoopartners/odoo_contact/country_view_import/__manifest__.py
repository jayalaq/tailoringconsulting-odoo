{
    'name': 'Country View Import',
    'version': '17.0.1.3.0',
    'author': 'Ganemo',
    'website': 'https://www.ganemo.co',
    'category': 'Other Extra Rights/Other Extra Rights',
    'summary': 'Custom country view with in-UI create and delete functionality',
    'description': """
This module creates a custom view that inherits from the standard countries view and 
adds the ability to create and delete country records directly from the user interface. 

To find the custom view, navigate to the following path: Contacts Module / Settings, then select "Countries" from the menu.
""",
    'depends': [
        'base'
    ],
    'data': [
        'views/res_country_views.xml'
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
    'license': 'Other proprietary',
    'currency': 'USD',
    'price': 20.00
}

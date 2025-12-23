{
    'name': 'DUA in Invoice',
    'version': '17.0.1.1.0',
    'author': 'Ganemo',
    'website': 'https://www.ganemo.co',
    'category': 'Accounting/Accounting',
    'summary': 'Add required fields on purchase invoices to register the DUA as required by the electronic purchase record (PLE).',
    'description': """
This module will create the field called "Year of issue" and "Customs unit" in the supplier invoice when we choose the document type "50" called "SAD".

In the field "Customs Unit" it will give us a list of codes: 019, 028, 046, 055, 082, etc.

*These codes will be loaded in the path "LOCATION/PLE/[11]CUSTOMS DEPENDENCY CODE".
    """,
    'depends': [
        'localization_menu',
        'purchase_document_type_validation'
    ],
    'data': [
        'views/account_move_views.xml',
        'data/account_move_data.xml',
    ],
    'application': False,
    'installable': True,
    'auto_install': False,
    'license': 'Other proprietary',
    'currency': 'USD',
    'price': 10.00
}

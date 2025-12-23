{
    'name': 'Print Additional Comment',
    'version': '17.0.1.1.1',
    'author': 'Ganemo',
    'website': 'https://www.ganemo.co',
    'category': 'Invoicing/Invoicing',
    'summary': 'Additional information in the invoice report',
    'description': """
This module creates a new tab called "Additional Information Printed Invoice" which is loated 
in the path: Module Settings / Users and Companies / Companies. There you will find said tab 
that will be created when installing de module where you can enter free text as desired, that 
the client needs. Its funtionality will be to create a free text box in the invoice report.
    """,
    'depends': [
        'account'
    ],
    'data': [
        'reports/report_invoice_document.xml',
        'views/res_company_views.xml'
    ],
    'application': False,
    'installable': True,
    'auto_install': False,
    'license': 'Other proprietary',
    'currency': 'USD',
    'price': 20.00
}

{
    'name': 'Add reconcile date',
    'version': '17.0.1.0.0',
    'author': 'Ganemo',
    'website': 'https://www.ganemo.co',
    'summary': 'Add Reconciliation Date Field',
    'Description': '''
    This module creates the “Reconciliation Date” field, meaning that when we reconcile records, the date on which they were reconciled will be entered.
    When we reconcile records, Odoo will give you a complete reconciliation number with which when we go to our complete reconciliations we can identify them and see the records that were made on that date.
    ''',
    'category': 'All',
    'depends': ['account'],
    'data': ['views/reconcile_views.xml'],
    'installable': True,
    'auto_install': False,
    'application': False,
    'license': 'Other proprietary',
    'currency': 'USD',
    'price': 10.99
}

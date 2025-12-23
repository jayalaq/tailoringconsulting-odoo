{
    'name': 'RUC Validation SUNAT',
    'version': '17.0.1.0.0',
    'author': 'Ganemo',
    'website': 'https://www.ganemo.co',
    'summary': 'This module creates a connection to the RUC query service.',
    'category': 'Accounting',
    'module_type': 'official',
    'depends': [
        'document_type_validation',
        'l10n_pe_catalog',
        'first_and_last_name',
        'l10n_country_filter'
    ],
    'data': [
        'views/partner_views.xml',
        'security/ir.model.access.csv'
    ],
    'installable': True,
    'auto_install': False,
    'license': 'Other proprietary',
    'currency': 'USD',
    'price': 4.00
}

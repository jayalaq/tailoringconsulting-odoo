{
    'name': 'Pago Masivo Proveedores',
    'version': '17.0.1.0.2',
    'module_type': 'official',
    'author': 'Ganemo',
    'website': 'https://www.ganemo.co',
    'live_test_url': 'https://www.ganemo.co/demo',
    'description': 'This module issues the txt files for the massive payment of suppliers',
    'summary': 'This module issues the txt files for the massive payment of suppliers',
    'depends': [
        'l10n_pe_edi',
        'financial_entity_sunat_code',
        'base_spot',
        'type_bank_accounts',
        'account_batch_payment',
    ],
    'data': [
        'views/account_batch_payment.xml'
    ],
    'installable': True,
    'auto_install': False,
    'license': 'Other proprietary',
    'currency': 'USD',
    'price': 0.00,
}

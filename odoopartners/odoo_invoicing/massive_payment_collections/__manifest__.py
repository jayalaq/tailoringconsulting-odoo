{
    "name": "Registro de pagos y cobros desde apuntes contables",
    "version": "17.0.1.0.2",
    "author": "Ganemo",
    "website": "https://www.ganemo.co",
    "live_test_url": "https://www.ganemo.co",
    "summary": "Module for mass collections/payments.",
    'description': """
        This module will be used to make massive collections and payments from the accounting notes,
        it will create the accounting entries in the payments of suppliers and clients.
    """,
    "category": "Accounting",
    "depends": [
        "account",
        "account_field_to_force_exchange_rate"
    ],
    'data': [
        'security/ir.model.access.csv',
        'wizards/massive_payment_collections_views.xml'
    ],
    "installable": True,
    "auto_install": False,
    "application": False,
    "license": "Other proprietary",
    "currency": "USD",
    "price": 50.00,
    "module_type": "official", 
}

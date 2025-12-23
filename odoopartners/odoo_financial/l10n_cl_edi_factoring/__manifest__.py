{
    "name": """Factoring for Chile""",
    'version': '17.0.1.0.0',
    'category': 'Localization/Chile',
    'sequence': 12,
    'author':  'Ganemo',
    'website': 'https://www.ganemo.co',
    'license': 'Other proprietary',
    'summary': '',
    'description': """
Factoring for Chile.
""",
    'depends': [
        'l10n_cl_edi',
    ],
    'external_dependencies': {
        'python': [
            'facturacion_electronica',
        ]
    },
    'data': [
        'views/account_move_view.xml',
    ],
    'module_type': 'official',
    'installable': True,
    'auto_install': False,
    'application': True,
}

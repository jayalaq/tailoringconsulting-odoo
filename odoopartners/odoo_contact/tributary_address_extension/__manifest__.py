{
    'name': 'Tributary Address Extension',
    'version': '17.0.1.3.1',
    'author': 'Ganemo',
    'website': 'https://www.ganemo.co',
    'category': 'Localization/Localization',
    'summary': 'Add the field "Establishment Annex" in contact',
    'description': """
This module will add the field "Establishment Annex" in the contact form.
This field will only be displayed if the set country for the company is Peru; otherwise, it won't appear.
This field is a dependency for many modules of the Peruvian localization such as electronic invoicing.
    """,
    'depends': [
        'l10n_country_filter',
    ],
    'data': [
        'views/res_partner_views.xml'
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
    'license': 'Other proprietary',
    'currency': 'USD',
    'price': 20.00
}

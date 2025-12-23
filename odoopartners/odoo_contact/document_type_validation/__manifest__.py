{
    'name': 'Document Type Validation',
    'version': '17.0.1.3.0',
    'author': 'Ganemo',
    'website': 'https://www.ganemo.co',
    'category': 'Localization/Localization',
    'summary': 'Manage validations for any location',
    'description': """
This Module manages and relates the type of document required by SUNAT (DNI, RUC, others) inherited object 'l10n_latam.identification.type'. Additionally, add validation, when saving a 'res.partner', and when making a change to the 'vat' field , or 'document_type_id' of 'res.partner', which does not meet the conditions of the parameters in the new fields created above.

The module creates 4 fields in the model 'l10n_latam.identication.type':

- doc_length  : This attribute refers to the specific length that a document must have.
- doc_type    : This attribute specifies the type of document expected in a field.
- exact_length: This attribute refers to the precise length that a document must be.
- nationality : This attribute refers to the nationality associated with a document.

Odoo's VAT number validation module for Latin American countries verifies that the VAT numbers of partners (customers and suppliers) are valid according to the regulations of the corresponding countries.

The module performs two checking functions:

- Length   : The VAT number must have the correct length according to the type of identification of the member.
- Structure: The VAT number must have the correct structure according to the type of identification of the partner.

If any error is found during validation, the module displays an error message and clears the partner vat field. 
""",
    'depends': [
        'l10n_latam_base'
    ],
    'data': [
        'views/l10n_latam_identification_type_views.xml',
        'views/res_partner_views.xml'
    ],
    'assets': {
        'web.assets_backend': [
            'document_type_validation/static/src/css/main.css',
        ],
    },
    'application': False,
    'installable': True,
    'auto_install': False,
    'license': 'Other proprietary',
    'currency': 'USD',
    'price': 20.00
}

{
    'name': ' Electronic Sales Record (PLE)',
    'version': '17.0.1.0.8',
    'author': 'Ganemo',
    'website': 'https://www.ganemo.co',
    'category': 'Accounting',
    'summary': 'Submit your sales book to SUNAT through PLE.',
    'description': """
This module called “PLE reports” has been created to generate PLE sales reports for which it will contain an object called account.account.tag and will serve to position the information from the sales book in the columns.
It will contain these fields

- Field company_id “Company” of type many2one
- Field date_start “start date” of type date
- Field date_end “end date” of type date
- Field bool_consolidate_pos “Daily POS consolidation? of type boolean
- Field state_send “sending status” of type selection NOTE: This field must be activated when the next module is installed. SEE
- Field date_ple “Generated on” of type date.
- Field xls_binary “excel report” of type binary and this will contain information that will be explained later.
- Field txt_binary “report .TXT” of type binary and this will contain information that will be explained later.

The .txt, .xlsx files must be generated successfully
""",
    'depends': [
        'l10n_country_filter',
        'account_origin_invoice',
        'dua_in_invoice',
        'account_exchange_currency',
        'l10n_pe',
    ],
    'data': [
        'security/ir_rule.xml',
        'security/ir.model.access.csv',
        'data/account_tax_report_data.xml',
        'data/account_tax_tags.xml',
        'views/account_account_views.xml',
        'views/account_journal_views.xml',
        'views/account_move_views.xml',
        'views/ple_report_sale_views.xml',
        'views/res_company_views.xml',
        'views/uom_uom_views.xml',
        'views/menu_ple_menus.xml',
        'views/ple_report_sale_menus.xml',
        'sql/get_tax.sql',
        'sql/validate_string.sql',
        'sql/validate_spaces.sql'
    ],
    'installable': True,
    'auto_install': False,
    'post_init_hook': '_combined_post_init_hook',
    'license': 'Other proprietary',
    'module_type': 'official',
    'currency': 'USD',
    'price': 360.00
}

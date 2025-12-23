{
    'name': 'Cashier only uses his diaries',
    'version': '17.0.1.1.1',
    'author': 'Ganemo',
    'website': 'https://www.ganemo.co',
    'category': 'Accounting',
    'summary': "Restricted Journal Records for Assigned Users",
    'description': """
In each Journal you assign one or more assigned users and when a user uses a Payment button, he will only see his assigned Cash and Bank journals.
In the dashboard view, only those journals in which it has been assigned will appear to the user.
""",
    'depends': [
        'account'
    ],
    'data': [
        'security/add_user_by_journal_res_group.xml',
        'security/add_user_by_journal_ir_rule.xml',
        'views/account_journal_views.xml'
    ],
    'uninstall_hook': '_uninstall_module_complete',
    'application': False,
    'installable': True,
    'auto_install': False,
    'license': 'Other proprietary',
    'currency': 'USD',
    'price': 25.00,
    'module_type': 'official',
}

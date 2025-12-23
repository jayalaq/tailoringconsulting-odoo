from odoo import models, fields, api, _


class AccountJournal(models.Model):
    _inherit = 'account.journal'

    default_credit_account_id = fields.Many2one(
        'account.account',
        string='Cuenta acreedora por defecto',
        domain=[('deprecated', '=', False)]
    )
    default_debit_account_id = fields.Many2one(
        'account.account',
        string='Cuenta deudora por defecto',
        domain="[('deprecated', '=', False), ('company_id', '=', company_id)]"
    )
    sequence_number_next = fields.Integer(
        string='Próximo número'
    )


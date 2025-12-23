from odoo import fields, models,api


class AccountAccount(models.Model):
    _inherit = 'account.account'

    ple_selection = fields.Selection(
        selection_add=[
            ("cash", "1.1 Libro Caja y Bancos: Efectivo"),
            ("bank", "1.2 Libro Caja y Bancos: Cuentas corrientes")]
    )
    bank_id = fields.Many2one(
        comodel_name='res.partner.bank',
        string='Cuenta Bancaria'
    )


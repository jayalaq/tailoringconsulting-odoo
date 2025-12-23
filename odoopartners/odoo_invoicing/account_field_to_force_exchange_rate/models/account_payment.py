from odoo import fields, models, api


class AccountPayment(models.Model):
    _inherit = 'account.payment'

    to_force_exchange_rate_template = fields.Float(
        string='Forzar T.C.',
        digits=(12, 12),
        help='Este campo se utiliza para forzar el tipo de cambio.',
        compute='_compute_move_id_to_force_exchange_rate',
    )

    to_force_exchange_rate = fields.Float(
        string='Forzar T.C.',
        digits=(12, 12),
        help='Este campo se utiliza para forzar el tipo de cambio.',
        store=True
    )

    @api.depends('move_id')
    def _compute_move_id_to_force_exchange_rate(self):
        move_temp = self.env['account.move'].search([('name', '=', self.ref)])
        self.to_force_exchange_rate_template = move_temp.to_force_exchange_rate if move_temp.to_force_exchange_rate else move_temp.exchange_rate
        self.move_id.exchange_rate = move_temp.exchange_rate if move_temp.exchange_rate else 0.0
        self.move_id.to_force_exchange_rate = move_temp.to_force_exchange_rate if move_temp.to_force_exchange_rate else 0.0
        self.to_force_exchange_rate = self.to_force_exchange_rate_template
        
    @api.onchange('currency_id', 'company_id', 'to_force_exchange_rate')
    def _onchange_to_force_exchange_rate(self):
        if self.currency_id == self.company_currency_id:
            self.to_force_exchange_rate = 0.0

    def _force_exchange_rate_verification(self):
        different_currency = self.currency_id and self.currency_id != self.company_currency_id
        force_exchange_rate = self.to_force_exchange_rate != 0.0 and self.to_force_exchange_rate != self.exchange_rate
        return different_currency and force_exchange_rate

    def _prepare_move_line_default_vals(self, write_off_line_vals=None, force_balance=None):
        line_vals_list = super(AccountPayment, self)._prepare_move_line_default_vals(write_off_line_vals, force_balance)

        if self._force_exchange_rate_verification():
            for line_vals in line_vals_list:
                liquidity_amount_currency = line_vals.get('amount_currency', 0.0)
                liquidity_balance = self.currency_id._force_convert(
                    liquidity_amount_currency,
                    self.company_id.currency_id,
                    self.company_id,
                    self.to_force_exchange_rate
                )
                line_vals.update({
                    'debit': liquidity_balance if liquidity_balance > 0.0 else 0.0,
                    'credit': -liquidity_balance if liquidity_balance < 0.0 else 0.0,
                })

        return line_vals_list

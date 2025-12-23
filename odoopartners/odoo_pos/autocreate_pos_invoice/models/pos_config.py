from odoo import fields, models


class PosConfig(models.Model):
    _inherit = 'pos.config'

    def _default_ticket_journal(self):
        return self.env['account.journal'].search([
            *self.env['account.journal']._check_company_domain(self.env.company),
            ('type', '=', 'sale'),
        ], limit=1)

    always_move_account = fields.Boolean(
        string='Create Seat For Each Ticket'
    )
    ticket_partner_id = fields.Many2one(
        comodel_name='res.partner',
        string='Default Partner'
    )
    invoice_journal_id = fields.Many2one(
        domain=False
    )
    ticket_journal_id = fields.Many2one(
        comodel_name='account.journal',
        string='Journal Tickets',
        check_company=True,
        domain=False,
        default=_default_ticket_journal
    )

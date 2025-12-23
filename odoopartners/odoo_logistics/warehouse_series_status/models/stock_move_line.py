from odoo import models, fields, api


class StockMoveLine(models.Model):
    _inherit = 'stock.move.line'

    status = fields.Many2one(
        comodel_name='stock.production.lot.status',
        string='Status',
        compute='_compute_status',
        inverse='_inverse_status',
        readonly=False,
        store=True
    )

    @api.depends('lot_id')
    def _compute_status(self):
        for record in self:
            if record.lot_id and record.lot_id.status:
                record.status = record.lot_id.status
            else:
                record.status = False

    def _inverse_status(self):
        pass
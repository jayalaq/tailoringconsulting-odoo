from odoo import models, fields, api


class StockQuant(models.Model):
    _inherit = 'stock.quant'

    status = fields.Char(
        string='Status',
        compute='_compute_status',
        readonly=True,
        store=True
    )

    @api.depends('lot_id')
    def _compute_status(self):
        for record in self:
            if record.lot_id.status.code and record.lot_id.status.name:
                record.status = "%s - %s" % (record.lot_id.status.code, record.lot_id.status.name)
            else:
                record.status = ''
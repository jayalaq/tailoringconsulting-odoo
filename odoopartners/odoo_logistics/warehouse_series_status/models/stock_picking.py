from odoo import models


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    def button_validate(self):
        res = super().button_validate()
        for line in self.move_line_ids_without_package:
            if line.lot_id and line.status:
                line.lot_id.status = line.status
        return res

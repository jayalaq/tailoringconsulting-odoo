from odoo import api, fields, models
import math


class StockMove(models.Model):
    _inherit = 'stock.move'

    def update_qty_initial_demand(self, product_id):
        for rec in self:
            if rec.state != 'cancel':
                rec.product_uom_qty = rec.product_uom_qty + (rec.product_uom_qty * (product_id.waste_mo_increment/100))
                #rec.quantity = rec.quantity + (rec.quantity * (product_id.waste_mo_increment/100))
                if rec.product_uom.active_round:
                    rec.product_uom_qty = math.ceil(rec.product_uom_qty)
                    #rec.quantity = math.ceil(rec.quantity)                    
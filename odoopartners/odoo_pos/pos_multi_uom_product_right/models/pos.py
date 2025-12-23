from odoo import fields, models


class PosSession(models.Model):
    _inherit = 'pos.session'

    def _loader_params_product_product(self):
        search_params = super()._loader_params_product_product()
        search_params['search_params']['fields'].extend(
            ['has_multi_uom', 'show_all_uom', 'allow_uoms', 'uom_category_id'])
        return search_params


class PosConfig(models.Model):
    _inherit = 'pos.config'

    allow_multi_uom = fields.Boolean(string='Product multi UOM', default=True)


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    has_multi_uom = fields.Boolean(string='Has multi UOM')
    show_all_uom = fields.Boolean(string='Show All UOM in POS')
    allow_uoms = fields.Many2many(
        'uom.uom', 
        'product_tmpl_uom', 
        'product_tmpl_id', 
        'product_uom_id', 
        string='Allow UOMS'
    )
    uom_category_id = fields.Many2one(
        'uom.category', 
        related='uom_id.category_id'
    )


class PosOrderLine(models.Model):
    _inherit = "pos.order.line"

    product_uom = fields.Many2one(
        'uom.uom', 
        string='Unit of measure'
    )

    def _order_line_fields(self, line, session_id=None):
        line = super(PosOrderLine, self)._order_line_fields(line, session_id)
        if line[2].get("product_uom", False) and isinstance(line[2]["product_uom"], dict):
            line[2]["product_uom"] = line[2]["product_uom"]["id"]
        elif 'is_selection_combo' in line[2].keys() and 'own_line' in line[2].keys():
            line[2]["product_uom"] = line[2]["own_line"][0][2]['product_uom']['id']
        elif 'product_uom_id' in line[2].keys() and 'product_uom' not in line[2].keys():
            line[2]["product_uom"] = line[2]["product_uom_id"]["id"]                
        else:
            if line[2].get("product_uom"):
                line[2]["product_uom"] = line[2]["product_uom"]
            else:
                product = self.env['product.template'].search([('name', '=', line[2]["full_product_name"])], limit=1)
                line[2]["product_uom"] = product.uom_id.id
        return line

    def _export_for_ui(self, orderline):
        export_ui = super()._export_for_ui(orderline)
        export_ui['product_uom'] = orderline.product_uom and orderline.product_uom.id
        return export_ui


class PosOrder(models.Model):
    _inherit = "pos.order"

    def _get_fields_for_order_line(self):
        fields = super(PosOrder, self)._get_fields_for_order_line()
        fields.extend(['product_uom'])
        return fields
    
    def _get_invoice_lines_values(self, line_values, pos_line):
        inv_line_vals = super()._get_invoice_lines_values(line_values, pos_line)
        inv_line_vals['product_uom_id'] = pos_line.product_uom.id
        return inv_line_vals


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    def _prepare_stock_move_vals(self, first_line, order_lines):
        return {
            'name': first_line.name,
            'product_uom': first_line.product_id.uom_id.id,
            'picking_id': self.id,
            'picking_type_id': self.picking_type_id.id,
            'product_id': first_line.product_id.id,
            'product_uom_qty': first_line.product_id.uom_id.factor * abs(sum(order_lines.mapped(lambda x: x.qty * x.product_uom.factor_inv))),
            'state': 'draft',
            'location_id': self.location_id.id,
            'location_dest_id': self.location_dest_id.id,
            'company_id': self.company_id.id,
        }

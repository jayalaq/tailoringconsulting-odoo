from odoo import models, api, _, fields
import math


class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    is_first_onchange = fields.Boolean(default=False, copy=False)

    def action_confirm(self):
        res = super(MrpProduction, self).action_confirm()
        for mrp in self:
            for pick in mrp.picking_ids:
                if mrp.location_src_id == pick.location_dest_id:
                    for move in pick.move_ids_without_package:
                        if move.rule_id.extra_pt:
                            move.update_qty_initial_demand(self.product_id)
                pick.action_assign()
        return res

    @api.onchange("qty_producing")
    def _onchange_qty_producing(self):
        for mrp in self:                          
            if mrp.state != 'draft':
                mrp.is_first_onchange = True
                mrp.update_data_lines(True)           

    @api.onchange("move_raw_ids", "move_raw_ids.product_uom_qty", "move_raw_ids.quantity")
    def _onchange_move_raw_ids_recalculate(self):
        for mrp in self:                          
            mrp.update_data_lines(True)
                        
    def to_write_update(self):
        for mrp in self:                          
            mrp.update_data_lines()
    
    def update_data_lines(self, assign_picking=False):
        for mrp in self: 
            for pick in mrp.picking_ids:
                new_moves = []
                for line in mrp.move_raw_ids:
                    if mrp.location_src_id == pick.location_dest_id:                        
                        existing_product_ids = pick.move_ids_without_package.mapped('product_id.id')
                        if line.product_id.id not in existing_product_ids:
                            new_moves.append((0, 0, {
                                'product_id': line.product_id.id,
                                'name': line.product_id.display_name,
                                'date': pick.scheduled_date,
                                'quantity': line.quantity,
                                'description_picking': line.product_id.display_name,
                                'location_id': pick.location_id.id,
                                'location_dest_id': pick.location_dest_id.id,
                            }))     
                if new_moves:
                    pick.write({'move_ids_without_package': new_moves})
                #pick.action_assign()
            for pick in mrp.picking_ids:
                for line in mrp.move_raw_ids:
                    for move in pick.move_ids_without_package:
                        if mrp.location_dest_id == pick.location_id and mrp.product_id == move.product_id and move.state != 'cancel':
                            #move.quantity = mrp.qty_producing
                            move.product_uom_qty = mrp.qty_producing
                            if move.product_uom.active_round:
                                #move.quantity = math.ceil(move.quantity)
                                move.product_uom_qty = math.ceil(move.product_uom_qty)
                        if mrp.location_src_id == pick.location_dest_id and line.product_id == move.product_id and move.state != 'cancel':
                            move.product_uom_qty = line.quantity + (line.quantity * (mrp.product_id.waste_mo_increment/100))
                            #move.quantity = move.product_uom_qty                        
                            if move.product_uom.active_round:
                                #move.quantity = math.ceil(move.quantity)
                                move.product_uom_qty = math.ceil(move.product_uom_qty)
                if not assign_picking:
                    pick.action_assign()


                
    def update_data_lines_action(self):
        for mrp in self: 
            for pick in mrp.picking_ids:
                new_moves = []
                for line in mrp.move_raw_ids:
                    if mrp.location_src_id == pick.location_dest_id:                        
                        existing_product_ids = pick.move_ids_without_package.mapped('product_id.id')
                        if line.product_id.id not in existing_product_ids:
                            new_moves.append((0, 0, {
                                'product_id': line.product_id.id,
                                'name': line.product_id.display_name,
                                'date': pick.scheduled_date,
                                'quantity': line.quantity,
                                'description_picking': line.product_id.display_name,
                                'location_id': pick.location_id.id,
                                'location_dest_id': pick.location_dest_id.id,
                            }))     
                if new_moves:
                    pick.write({'move_ids_without_package': new_moves})
            for pick in mrp.picking_ids:
                for line in mrp.move_raw_ids:
                    for move in pick.move_ids_without_package:
                        if mrp.location_dest_id == pick.location_id and mrp.product_id == move.product_id and move.state != 'cancel':
                            #move.quantity = mrp.product_uom_qty
                            move.product_uom_qty = mrp.product_uom_qty
                            if move.product_uom.active_round:
                                #move.quantity = math.ceil(move.quantity)
                                move.product_uom_qty = math.ceil(move.product_uom_qty)

                        if mrp.location_src_id == pick.location_dest_id and line.product_id == move.product_id and move.state != 'cancel':
                            move.product_uom_qty = line.product_uom_qty + (line.product_uom_qty * (mrp.product_id.waste_mo_increment/100))   
                            #move.quantity = move.product_uom_qty                         
                            if move.product_uom.active_round:
                                #move.quantity = math.ceil(move.quantity)
                                move.product_uom_qty = math.ceil(move.product_uom_qty)
                pick.action_assign()


    @api.onchange("move_raw_ids")
    def _onchange_move_raw_ids_recalculate(self):
        for mrp in self:                          
            mrp.update_data_lines(True)

    def write(self, vals):
        res = super(MrpProduction, self).write(vals)
        self.to_write_update()
        return res

    def action_view_mo_delivery(self):
        """ Returns an action that display picking related to manufacturing order.
        It can either be a list view or in a form view (if there is only one picking to show).
        """
        self.ensure_one()
        action = self.env["ir.actions.actions"]._for_xml_id("stock.action_picking_tree_all")
        if len(self.picking_ids) > 1:
            action['domain'] = [('id', 'in', self.picking_ids.ids)]
        elif self.picking_ids:
            action['res_id'] = self.picking_ids.id
            action['views'] = [(self.env.ref('stock.view_picking_form').id, 'form')]
            if 'views' in action:
                action['views'] += [(state, view) for state, view in action['views'] if view != 'form']
        action['context'] = dict(self._context, default_origin=self.name)

        if not self.is_first_onchange:
            self.update_data_lines_action()
        return action
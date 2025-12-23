from odoo import models, fields, api
from odoo.exceptions import UserError


class StockWarehouse(models.Model):
    _inherit = 'stock.warehouse'
    user_ids = fields.Many2many('res.users', string='Asignado a ')

    
class StockLocation(models.Model):
    _inherit = 'stock.location'

    user_ids_01 = fields.Many2many('res.users', string='Asignado a ')
    user_ids_02 = fields.Many2many('res.users', relation='responsable_', string='Responsable')


class StockPickingType(models.Model):
    _inherit = 'stock.picking.type'
    users_warehouse_id = fields.Many2many('res.users', string='Asignado a ', related='warehouse_id.user_ids')


class StockPicking(models.Model):
    _inherit = 'stock.picking'
    
    def _default_picking_type_id(self):
        picking_type_code = self.env.context.get('restricted_picking_type_code')
        if picking_type_code:
            user = self.env.user
            picking_types = self.env['stock.picking.type'].search([
                ('code', '=', picking_type_code),
                ('company_id', '=', self.env.company.id),
                '|',
                ('warehouse_id.user_ids', 'in', user.id),
                ('warehouse_id.user_ids', '=', False),
            ])
            return picking_types[:1].id

    user_logger = fields.Many2one('res.users', string='Asignado a ', default=lambda self: self.env.user, required=True, store=True)
    picking_type_id = fields.Many2one(
        comodel_name='stock.picking.type',
        required=True,
        check_company=True,
        default=_default_picking_type_id,
        index=True)

    location_id = fields.Many2one(
        comodel_name='stock.location',
        string='Source Location',
        required=True)

    
    @api.depends('picking_type_id', 'partner_id')
    def _compute_location_id(self):
        for picking in self:
            picking = picking.with_company(picking.company_id)
            if picking.picking_type_id and picking.state == 'draft':
                if picking.picking_type_id.default_location_src_id :
                    location_id = picking.picking_type_id.default_location_src_id.id
                elif picking.partner_id:
                    location_id = picking.partner_id.property_stock_supplier.id
                else:
                    _customerloc, location_id = self.env['stock.warehouse']._get_partner_locations()

                if picking.picking_type_id.default_location_dest_id:
                    location_dest_id = picking.picking_type_id.default_location_dest_id.id
                elif picking.partner_id:
                    location_dest_id = picking.partner_id.property_stock_customer.id
                else:
                    location_dest_id, _supplierloc = self.env['stock.warehouse']._get_partner_locations()

                location = self.env['stock.location'].search([('id', '=', int(location_id))], limit=1)
                if picking.user_logger in location.user_ids_01  or not location.user_ids_01:
                    picking.location_id = location_id
                    picking.location_dest_id = location_dest_id


    @api.model
    def _get_view(self, view_id=None, view_type='form', **options):
        arch, view = super()._get_view(view_id, view_type, **options)

        if view_type == 'form':
            user = self.env.user
            for node in arch.xpath("//field[@name='picking_type_id']"):
                domain = "[ '|', ('warehouse_id.user_ids', 'in', %s), ('warehouse_id.user_ids', '=', False)]" % (user.id)
                node.set('domain', domain)

            for node in arch.xpath("//field[@name='location_id']"):
                domain = "[ '|', ('user_ids_01', 'in', %s), ('user_ids_01', '=', False)]" % (user.id)
                node.set('domain', domain)

        return arch, view
    

    def button_validate(self):
        message = "No puedes validar esta transacción, porque no eres el usuario responsable de " \
                  "la ubicación a la que estás enviando la Mercadería. Comunícate con el usuario responsable de " \
                  "la ubicación de Destino para que valide esta transacción."
        user = self.env.user

        if len(self.location_dest_id.user_ids_02) == 0:
            return super(StockPicking, self).button_validate()
        else:
            for i in range(len(self.location_dest_id.user_ids_02)):
                if self.location_dest_id.user_ids_02[i].id == user.id:
                    return super(StockPicking, self).button_validate()
        raise UserError(message)

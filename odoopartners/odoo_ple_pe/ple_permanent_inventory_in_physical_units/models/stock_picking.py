from odoo import api, models, fields, _
from odoo.tools import float_round

stock_picking_reason = [
    ('01', "[01] Venta Nacional"),
    ('02', "[02] Compra Nacional"),
    ('03', "[03] Consignación Recibida"),
    ('04', "[04] Consignación Entregada"),
    ('05', "[05] Devolución Recibida"),
    ('06', "[06] Devolución Entregada"),
    ('07', "[07] Bonificación"),
    ('08', "[08] Premio"),
    ('09', "[09] Donación"),
    ('10', "[10] Salida a Producción"),
    ('11', "[11] Salida Transferencia entre almacenes"),
    ('12', "[12] Retiro"),
    ('13', "[13] Mermas"),
    ('14', "[14] Desmedros"),
    ('15', "[15] Destrucción"),
    ('16', "[16] Saldo Inicial"),
    ('17', "[17] Exportación"),
    ('18', "[18] Importación"),
    ('19', "[19] Entrada de Producción"),
    ('20', "[20] Entrada devolución de producción"),
    ('21', "[21] Entrada Transferencia entre almacenes"),
    ('22', "[22] Entrada por identificación erronea"),
    ('23', "[23] Salida por identificación erronea"),
    ('24', "[24] Entrada por devolución del cliente"),
    ('25', "[25] Salida por devolución al proveedor"),
    ('26', "[26] Entrada para servicio de producción"),
    ('27', "[27] Salida por servicio de producción"),
    ('28', "[28] Ajuste por diferencia de inventario"),
    ('29', "[29] Entrada de bienes en préstamo"),
    ('30', "[30] Salida de bienes en préstamo"),
    ('31', "[31] Entrada de bienes en custodia"),
    ('32', "[32] Salida de bienes en custodia"),
    ('33', "[33] Muestras Médicas"),
    ('34', "[34] Publicidad"),
    ('35', "[35] Gastos de representación"),
    ('36', "[36] Retiro para entrega a trabajadores"),
    ('37', "[37] Retiro por convenio colectivo"),
    ('38', "[38] Retiro por sustitución de bien siniestrado"),
    ('99', "[99] Otros")
]


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    type_operation_sunat = fields.Selection(
        selection=stock_picking_reason,
        string='Tipo de Operación SUNAT'
    )

    @api.model_create_multi
    def create(self, vals_list):
        records = super(StockPicking, self).create(vals_list)
        for record in records:
            if not record.type_operation_sunat:
                record.onchange_type_operation_sunat()
        return records

    @api.onchange('location_id', 'location_dest_id', 'picking_type_id')
    def onchange_type_operation_sunat(self):
        if self.picking_type_id:
            code = self.picking_type_id.code
            flag1 = self.check_picking_type_id_code(self.location_id, code)
            flag2 = self.check_picking_type_id_code(self.location_dest_id, code)
            if flag1 and flag2:
                self.type_operation_sunat = self.picking_type_id.ple_revert_id
            else:
                self.type_operation_sunat = self.picking_type_id.ple_reason_id

    @staticmethod
    def check_picking_type_id_code(location, code):
        if location and location.usage == code:
            return True
        else:
            return False

    @api.model
    def _get_view(self, view_id=None, view_type='form', **options):
        arch, view = super()._get_view(view_id, view_type, **options)
        if view_type in ('form'):
            tags = [('field', 'type_operation_sunat')]
            arch, view = self.env['res.partner']._tags_invisible_per_country(arch, view, tags, [self.env.ref('base.pe')])
        return arch, view


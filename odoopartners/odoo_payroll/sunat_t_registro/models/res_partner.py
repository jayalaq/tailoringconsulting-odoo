from odoo import api, fields, models

class ResPartner(models.Model):
    _inherit = 'res.partner'

    road_type = fields.Many2one('road.type.object', string='Tipo de Vía')
    road_name = fields.Char(string='Nombre de Vía')
    road_number = fields.Char(string='Número de Vía')
    road_departament = fields.Char(string='Departamento')
    road_inside = fields.Char(string='Interior')
    road_mz = fields.Char(string='Manzana')
    road_batch = fields.Char(string='Lote')
    road_km = fields.Char(string='Kilómetro')
    road_block = fields.Char(string='Block')
    road_stage = fields.Char(string='Etapa')
    zone_type = fields.Many2one('zone.type.object', string='Tipo de Zona')
    zone_name = fields.Char(string='Nombre de Zona')
    zone_reference = fields.Char(string='Referencia')
    zone_ubigeo = fields.Many2one('ubigeo.reniec.object', string='Ubigeo')

    address_2 = fields.Boolean(string='Dirección 2')

    indicator_essalud = fields.Selection(string='Indicador Centro Asistencial EsSalud', selection=[
        ('01', 'Dirección 1'),
        ('02', 'Dirección 2'),
    ])

    road_type_2 = fields.Many2one('road.type.object', string='Tipo de Vía 2')
    road_name_2 = fields.Char(string='Nombre de Vía 2')
    road_number_2 = fields.Char(string='Número de Vía 2')
    road_departament_2 = fields.Char(string='Departamento 2')
    road_inside_2 = fields.Char(string='Interior 2')
    road_mz_2 = fields.Char(string='Manzana 2')
    road_batch_2 = fields.Char(string='Lote 2')
    road_km_2 = fields.Char(string='Kilómetro 2')
    road_block_2 = fields.Char(string='Block 2')
    road_stage_2 = fields.Char(string='Etapa 2')
    zone_type_2 = fields.Many2one('zone.type.object', string='Tipo de Zona 2')
    zone_name_2 = fields.Char(string='Nombre de Zona 2')
    zone_reference_2 = fields.Char(string='Referencia 2')
    zone_ubigeo_2 = fields.Many2one('ubigeo.reniec.object', string='Ubigeo 2')
    other_annexed_estab = fields.One2many(comodel_name='other.annexed.establishments', inverse_name='partner_id', string='Otros establecimientos anexos')
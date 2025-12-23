from odoo import api, fields, models

class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    situation = fields.Selection(
        string='Situación',
        selection=[
            ('0', 'Baja'),
            ('1', 'Activo o subsidiado'),
            ('2', 'Sin vínculo laboral con conceptos pendiente de liquidar'),
            ('3', 'Suspensión perfecta de labores'),
        ],
        groups='hr.group_hr_user'
    )
    sctr = fields.Selection(
        string='SCTR',
        selection=[
            ('0', 'Ninguno'),
            ('1', 'ONP'),
            ('2', 'Cía. privada'),
        ],
        groups='hr.group_hr_user'
    )
    rent_category = fields.Boolean(string="Rentas de 5ta categoría exoneradas", groups='hr.group_hr_user', )
    double_taxation = fields.Selection(
        string='Convenio para evitar la doble tributación',
        selection=[
            ('0', 'Ninguno'),
            ('1', 'Canada'),
            ('2', 'Chile'),
            ('3', 'Can'),
            ('4', 'Brasil'),
        ],
        groups='hr.group_hr_user'
    )
    category_employee = fields.Selection(
        string='Categoria de Empleado',
        selection=[
            ('1', 'Trabajador'),
            ('2', 'Pensionista'),
            ('4', 'Personal de terceros'),
            ('5', 'Personal en formacion'),
        ],
        default='1',
        groups='hr.group_hr_user'
    )
    eps_services_propios = fields.Selection(
        string='EPS/Servicios Propios',
        selection=[
            ('1', '20514372251   -   PERSALUD S.A. EPS (1)'),
            ('2', '20431115825   -   PACÍFICO S.A. EPS'),
            ('3', '20414955020   -   RÍMAC INTERNACIONAL S.A. EPS'),
            ('4', '0             -   SERVICIOS PROPIOS'),
            ('5', '20517182673   -   MAPFRE PERU S.A. EPS'),
            ('6', '20523470761   -   SANITAS PERU S.A. - EPS'),
            ('7', '20601978572   -   EPS, LA POSITIVA S.A. ENTIDAD PRESTADORA DE SALUD'),
        ],
        default='1',
        groups='hr.group_hr_user'
    )
    sctr_salud = fields.Selection(
        string='SCTR SALUD',
        selection=[
            ('1', 'Essalud'),
            ('2', 'EPS'),
        ],
        groups='hr.group_hr_user'
    )
    inv_eps = fields.Char(
        string='Health regime',
        groups='hr.group_hr_user',
        related='health_regime_id.code'
    )
    edu_inst = fields.Selection(
        string='Institución Educativa del Perú',
        selection=[
            ('si', 'SI'),
            ('no', 'NO'),
        ],
        groups='hr.group_hr_user'
    )
    edu_name_id = fields.Many2one(
        comodel_name='edu.name.object',
        string='Institución Educativa',
        groups='hr.group_hr_user'
    )
    edu_career_id = fields.Many2one('edu.career.object', string='Carrera', groups='hr.group_hr_user')
    edu_year_id = fields.Many2one('edu.year.graduation.object', string='Año de Graduación', groups='hr.group_hr_user')
    edu_bool = fields.Char(string='Academic degree', related='academic_degree_id.code', groups='hr.group_hr_user')
    other_annexed = fields.Many2many(
        comodel_name='other.annexed.establishments',
        string='Otros establecimientos anexos',
        domain="[('id', 'in', other_annexed_filter)]",
        groups='hr.group_hr_user'
    )
    other_annexed_filter = fields.Many2many(
        comodel_name='other.annexed.establishments',
        relation='filter_table_annexes',
        compute='_compute_filter_other_annexed',
        groups='hr.group_hr_user'
    )

    code_pas_country_id = fields.Char(
        string='País emisor',
        compute='_compute_code_pas_country_id',
        store=True,
        groups='hr.group_hr_user'
    )

    @api.depends('type_identification_id', 'type_identification_id.country_id')
    def _compute_code_pas_country_id(self):
        for record in self:
            if (
                record.type_identification_id and
                record.type_identification_id.country_id and
                record.type_identification_id.l10n_pe_vat_code == '7'
            ):
                record.code_pas_country_id = record.type_identification_id.country_id.cod_pas_only
            else:
                record.code_pas_country_id = "No se encontro el codigo de pais"
    
    @api.depends('address_id')
    def _compute_filter_other_annexed(self):
        for record in self:
            annexes = []
            if record.address_id and record.address_id.other_annexed_estab:
                for annex_record in record.address_id.other_annexed_estab:
                    annexes.append(annex_record.id)
            record.other_annexed_filter = annexes if annexes else False
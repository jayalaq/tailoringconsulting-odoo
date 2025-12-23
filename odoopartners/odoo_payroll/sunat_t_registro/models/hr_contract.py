from odoo import api, fields, models

class HrContract(models.Model):
    _inherit = 'hr.contract'

    periodicity = fields.Selection(string='Periodicidad', selection=[
        ('01', 'Mensual'),
        ('02', 'Quincenal'),
        ('03', 'Semanal'),
        ('04', 'Diaria'),
        ('05', 'Otros'),
    ])
    work_category = fields.Many2one('occupational.worker.category', string='Categoría ocupacional del trabajado')
    type_formative_modality = fields.Many2one('type.formative.modality.work', string='Tipo de modalidad formativa laboral')
    occupation_training_modality = fields.Many2one('occupation.work.personnel.training.modality', string='Ocupación de trabajo')
    health_insurance_contract = fields.Selection(string='Seguro médico', selection=[
        ('01', 'Essalud'),
        ('02', 'Privado'),
    ])
    mother_responsability = fields.Boolean(string="Madre con responsabilidad Familiar")
    type_professional_center = fields.Selection(string='Tipo de Centro de Formación Profesional', selection=[
        ('01', 'Centro educativo'),
        ('02', 'Universidad'),
        ('03', 'Instituto'),
        ('04', 'Otros'),
    ])

    displacemnent = fields.Boolean(string='Destaco o Desplazo')
    employer_id = fields.Many2one(comodel_name='res.partner', string='Empleador')
    date_from_displacement = fields.Date(string='Fecha de Inicio')
    date_to_displacement = fields.Date(string='Fecha de Fin')
    risk_activities = fields.Boolean(string='Actividades de riesgo')
    given_service = fields.Many2one(comodel_name='international.industrial.classification', string='Servicio Prestado')
    worker_type_pensioner_provider = fields.Many2one(comodel_name='worker.type.pensioner.provider',
                                                     string='Tipo de trabajador, penionista o prestador de servicios')
    other_annexed = fields.Many2one(comodel_name='other.annexed.establishments', string='Otros establecimientos anexos',
                                    domain="[('id', 'in', other_annexed_filter)]")
    other_annexed_filter = fields.Many2many(comodel_name='other.annexed.establishments', relation='filter_table_annexes',
                                            compute='_compute_filter_other_annexed')

    @api.depends('employee_id')
    def _compute_filter_other_annexed(self):
        annexes = []
        if self.employee_id.other_annexed:
            for record in self.employee_id.other_annexed:
                annexes.append(record.id)
            self.other_annexed_filter = annexes
        else:
            self.other_annexed_filter = False
            
from odoo import fields, models


class HrPayrollStructure(models.Model):
    _inherit = 'hr.payroll.structure'

    struct_days_ids = fields.Many2many(
        comodel_name='hr.work.entry.type',
        string='Reglas días',
        relation='struct_days_ids_hr_payroll_structure_hr_work_entry_type_rel',
    )

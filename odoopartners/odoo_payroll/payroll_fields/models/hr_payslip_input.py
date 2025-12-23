from dateutil.relativedelta import relativedelta
from lxml import etree
from odoo import models, fields, api


class HrPayslipInput(models.Model):
    _inherit = 'hr.payslip.input'

    date_from = fields.Date(
        string='Desde',
        related='payslip_id.date_from'
    )
    date_to = fields.Date(
        string='Hasta',
        related='payslip_id.date_to'
    )
    date_start = fields.Char(
        string='Mes/Año nómina',
        related='payslip_id.date_start'
    )
    date_start_dt = fields.Date(
        string='Mes de nómina',
        related='payslip_id.date_start_dt',
        store=True
    )
    employee_id = fields.Many2one(
        string='Empleado',
        related='contract_id.employee_id'
    )
    state = fields.Selection(
        string='Estado',
        related='payslip_id.state'
    )
    department_id = fields.Many2one(
        comodel_name='hr.department',
        string="Departmento",
        related='employee_id.department_id'
    )
    company_id = fields.Many2one(
        comodel_name='res.company',
        string="Compañia",
        related='contract_id.company_id',
    )
    disability = fields.Boolean(
        string='Discapacidad',
        related='employee_id.disability'
    )
    struct_id = fields.Many2one(
        comodel_name='hr.payroll.structure',
        string='Estructura',
        related='payslip_id.struct_id'
    )
 
    @api.model
    def _get_view(self, view_id=None, view_type='form', **options):
        arch, view = super(HrPayslipInput, self)._get_view(view_id, view_type, **options)
        hr_payslip = self.env['hr.payslip.line']
        if view_type in ('search'):
            arch = hr_payslip.set_filter_six_month_before(arch)
        return arch, view

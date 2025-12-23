from dateutil.relativedelta import relativedelta
from lxml import etree
from odoo import models, fields, api


class HrPayslipRun(models.Model):
    _inherit = 'hr.payslip.run'

    date_st_dt = fields.Date(
        string='Mes de nómina',
        compute='_compute_date_start'
    )

    @api.depends('date_start', 'date_end')
    def _compute_date_start(self):
        payslip = self.env['hr.payslip']
        for rec in self:
            if rec.date_start and rec.date_end:
                _, _, _, rec.date_st_dt = payslip.generate_date_start_month_year(rec.date_start, rec.date_end)
                
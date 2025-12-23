from odoo import fields, models


class HolidaysUpdateWizard(models.TransientModel):
    _name = 'holiday.update.wizard'
    _description = 'Actualizador de vacaciones'

    date = fields.Date(
        string='Date',
        required=True,
    )

    def action_generate_holidays(self):
        self._recalculate_holidays_per_new_interval()

    def _recalculate_holidays_per_new_interval(self):
        self.ensure_one()

        hr_employees = self.env['hr.employee'].search([
            ('company_id', '=', self.env.company.id),
            ('contract_id.state', '=', 'open'),
        ])

        for employee in hr_employees:
            new_interval_holiday = round(float(employee.holidays_per_year) / 12, 2)
            for leave_allocation in employee.hr_allocation_ids:
                for day in leave_allocation.accruement_ids:
                    if day.accrued_on >= self.date:
                        day.days_accrued = new_interval_holiday

                leave_allocation._recalculate_days()
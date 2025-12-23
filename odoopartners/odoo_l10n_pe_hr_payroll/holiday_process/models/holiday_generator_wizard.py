import logging
from datetime import datetime

import pytz
from dateutil.relativedelta import relativedelta

from odoo import api, fields, models

_logger = logging.getLogger(__name__)


def _convert_date_timezone_to_utc(user, date_order, format_time='%Y-%m-%d %H:%M:%S'):
    tz = pytz.timezone(user.tz) if user.tz else pytz.utc
    date_order = datetime.strptime(date_order, format_time)
    datetime_with_tz = tz.localize(date_order, is_dst=None)
    date_order = datetime_with_tz.astimezone(pytz.utc)
    date_order = datetime.strftime(date_order, format_time)
    return date_order


class HolidaysGeneratorWizard(models.TransientModel):
    _name = 'holiday.generator.wizard'
    _description = 'Generador de vacaciones'

    employees_ids = fields.Many2many(
        comodel_name='hr.employee',
        string='Empleados'
    )
    is_generated = fields.Boolean(
        string='Fue generado?'
    )
    set_period = fields.Boolean(
        string='Definir periodo'
    )
    date_from = fields.Date(
        string='Desde',
    )
    date_to = fields.Date(
        string='Hasta',
    )

    @api.onchange('set_period')
    def onchange_set_period(self):
        self.date_from = self.date_to = False

    def action_generate_holidays(self):
        if self.employees_ids:
            employees = self.employees_ids
        else:
            employees = self.env['hr.employee'].search([
                ('has_holidays', '=', True),
                ('service_start_date', '!=', False)
            ])
        arr_employee = []
        for employee in employees:
            start_date = employee.service_start_date
            end_tdate = employee.service_termination_date
            arr_employee = self.set_period_holidays(employee, start_date, end_tdate, arr_employee)
        arr_employee = list(set(arr_employee))
        form = self.env.ref('holiday_process.holiday_generator_wizard_view_form')
        return {
            'name': 'Empleados con vacaciones generadas',
            'res_model': self._name,
            'view_mode': 'form',
            'views': [(form.id, 'form')],
            'context': {'default_is_generated': True, 'default_employees_ids': arr_employee},
            'view_id': form.id,
            'type': 'ir.actions.act_window',
            'target': 'new'
        }

    def set_period_holidays(self, employee, start_date, end_tdate, arr_employee):
        today = fields.Date.today()
        end_date = start_date + relativedelta(months=12)
        start_date, end_date, arr_employee = self.generate_holidays(start_date, end_date, employee, arr_employee)

        if end_tdate:
            while start_date.year <= end_tdate.year:
                start_date, end_date, arr_employee = self.generate_holidays(start_date, end_date, employee, arr_employee)
        else:
            while end_date.year <= today.year or start_date.year <= today.year <= end_date.year:
                start_date, end_date, arr_employee = self.generate_holidays(start_date, end_date, employee, arr_employee)
        return arr_employee

    def generate_holidays(self, start_date, end_date, employee, arr_employee):
        years = [] if not self.set_period else list(range(self.date_from.year, self.date_to.year + 1))
        if start_date.year in years or not self.set_period:
            holiday_id = self.env.ref('holiday_process.hr_leave_type_23')
            rec = self.env['hr.leave.allocation'].search([
                ('from_date', '=', start_date),
                ('to_date', '=', end_date),
                ('holiday_status_id', '=', holiday_id.id),
                ('employee_id', '=', employee.id)
            ])
            if not rec:
                date_order_from = _convert_date_timezone_to_utc(self.env.user, '{} 00:00:00'.format(start_date))
                date_order_to = _convert_date_timezone_to_utc(self.env.user, '{} 00:00:00'.format(end_date))
                nro_days = int(employee.additional_days) + int(employee.holidays_per_year)
                allocation_id = self.env['hr.leave.allocation'].create({
                    'name': 'Vacaciones {} {}'.format(start_date, end_date),
                    'holiday_status_id': holiday_id.id,
                    'to_date': end_date,
                    'from_date': start_date,
                    'allocation_type': 'accrual',
                    'date_from': date_order_from,
                    'date_to': date_order_to,
                    'holiday_type': 'employee',
                    'employee_id': employee.id,
                    'number_of_days': 0,
                    'unit_per_interval': 'days',
                    'number_per_interval': nro_days / 12,
                    'interval_number': 1,
                    'interval_unit': 'months',
                    'state': 'confirm',
                    'deadline': end_date + relativedelta(months=8),
                })
                try:
                    allocation_id.state = 'validate'
                    allocation_id._update_accrual_allocation()
                except Exception as e:
                    _logger.info('Vacación no aprobada:\n  .Empleado: {}\n  .Asignación:{}\n  .Error:{}'.format(employee.name, allocation_id.id, e))
                arr_employee.append(employee.id)
        start_date += relativedelta(months=12)
        end_date = start_date + relativedelta(months=12)
        return start_date, end_date, arr_employee
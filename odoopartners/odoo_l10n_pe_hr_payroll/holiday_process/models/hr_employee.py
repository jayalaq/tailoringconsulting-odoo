from collections import defaultdict

from odoo import fields, models
from odoo.addons.resource.models.utils import timezone_datetime


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    has_holidays = fields.Boolean(
        string='Vacaciones',
        groups="hr.group_hr_user"
    )
    holidays_per_year = fields.Char(
        string='Días de vacaciones por año',
        groups="hr.group_hr_user"
    )
    additional_days = fields.Char(
        string='Días adicionales',
        groups="hr.group_hr_user"
    )
    hr_allocation_ids_old = fields.One2many(
        comodel_name='hr.leave.allocation',
        inverse_name='employee_id',
        string='Líneas Vacaciones',
        groups="hr.group_hr_user"
    )
    hr_allocation_ids = fields.Many2many(
        comodel_name='hr.leave.allocation',
        relation='hr_employee_hr_leave_allocation_rel',
        column1='hr_employee_id',
        column2='hr_leave_allocation_id',
        string='Vacation Allocation Lines',
        groups="hr.group_hr_user"
    )

    def _get_work_days_data_batch_all(self, from_datetime, to_datetime, calendar=None):
        resources = self.mapped('resource_id')
        mapped_employees = {e.resource_id.id: e.id for e in self}
        result = {}

        # las fechas y horas nativas se hacen explícitas en UTC
        from_datetime = timezone_datetime(from_datetime)
        to_datetime = timezone_datetime(to_datetime)

        mapped_resources = defaultdict(lambda: self.env['resource.resource'])
        for record in self:
            mapped_resources[calendar or record.resource_calendar_id] |= record.resource_id

        for calendar, calendar_resources in mapped_resources.items():
            day_total = calendar.with_context(holiday_status_id=True)._get_resources_day_total(from_datetime, to_datetime, calendar_resources)
            intervals = calendar.with_context(holiday_status_id=True)._attendance_intervals_batch(from_datetime, to_datetime, calendar_resources)

            for calendar_resource in calendar_resources:
                result[calendar_resource.id] = calendar._get_days_data(intervals[calendar_resource.id], day_total[calendar_resource.id])

        # convertir "resource: result" en "employee: result"
        return {mapped_employees[r.id]: result[r.id] for r in resources}
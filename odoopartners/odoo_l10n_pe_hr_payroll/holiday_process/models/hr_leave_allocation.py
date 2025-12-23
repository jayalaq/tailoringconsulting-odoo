import logging

from odoo import api, fields, models
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)


class HrLeaveAllocation(models.Model):
    _inherit = 'hr.leave.allocation'

    to_date = fields.Date(
        string='Hasta'
    )
    from_date = fields.Date(
        string='Desde'
    )
    deadline = fields.Date(
        string='Tope de disfrute'
    )
    is_holiday = fields.Boolean(
        string='Es vacación?',
        compute='_compute_is_holiday',
        store=True
    )
    absence_ids = fields.One2many(
        comodel_name='hr.leave',
        inverse_name='hr_leave_id',
        string='Ausencias'
    )
    computed_holiday = fields.Float(
        string='Vacaciones computadas',
        compute='compute_days_holiday',
        store=True
    )
    used_holiday = fields.Float(
        string='Vac. gozadas o pagadas',
        compute='compute_days_holiday',
        store=True
    )
    pending_holiday = fields.Float(
        string='Vacaciones pendientes',
        compute='compute_days_holiday',
        store=True
    )

    def _recalculate_days(self):
        total_days = 0
        for rec in self.accruement_ids:
            total_days += rec.days_accrued
        self.computed_holiday = total_days - self.used_holiday
        self.pending_holiday = self.computed_holiday

    @api.depends('number_of_days_display', 'absence_ids', 'absence_ids.number_of_days_display', 'absence_ids.state')
    def compute_days_holiday(self):
        for rec in self:
            current_computed_holiday = rec.computed_holiday
            
            rec.computed_holiday = rec.number_of_days_display 
            current_used_holiday = sum(
                line.number_of_days_display for line in rec.absence_ids)
            
            rec.used_holiday = current_used_holiday
              
            if rec.number_of_days_display == 0.0:  
                rec.computed_holiday = current_computed_holiday
                rec.number_of_days = current_computed_holiday
                
            rec.pending_holiday = rec.computed_holiday - rec.used_holiday

    @api.depends('holiday_status_id')
    def _compute_is_holiday(self):
        holiday_id = self.env.ref('holiday_process.hr_leave_type_23', False)
        if holiday_id:
            for rec in self:
                if rec.holiday_status_id and rec.holiday_status_id == holiday_id:
                    rec.is_holiday = True

    def unlink(self):
        for rec in self:
            if rec.absence_ids:
                raise ValidationError('Primero debe eliminar las ausencias relacionadas.')
        return super(HrLeaveAllocation, self).unlink()

    def action_create_absence_holiday(self):
        holiday_id = self.env.ref('holiday_process.hr_leave_type_23')
        for rec in self:
            if rec.state == 'validate' or rec.state == 'validate1' and rec.holiday_status_id == holiday_id and \
                    rec.pending_holiday > 0:
                try:
                    self.env['hr.leave'].create({
                        'holiday_status_id': rec.holiday_status_id.id,
                        'employee_id': rec.employee_id.id,
                        'holiday_type': 'employee',
                        'hr_leave_id': rec.id
                    })
                except Exception as e:
                    _logger.warning(e)
                    continue
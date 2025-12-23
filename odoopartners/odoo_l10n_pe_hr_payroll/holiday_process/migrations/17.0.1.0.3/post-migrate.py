# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import api, SUPERUSER_ID

import logging

_logger = logging.getLogger(__name__)


def migrate(cr, version):
    env = api.Environment(cr, SUPERUSER_ID, {})
    
    env.cr.execute("DELETE FROM hr_employee_hr_leave_allocation_rel")

    employees = env['hr.employee'].search([])
    for employee in employees:
        employee.hr_allocation_ids = [(6, 0, employee.hr_allocation_ids_old.ids)]
    _logger.info("Migration of hr_allocation_ids completed successfully.")
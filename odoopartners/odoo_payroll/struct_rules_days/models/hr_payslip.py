from odoo import models


class HrPayslip(models.Model):
    _inherit = 'hr.payslip'

    def _get_new_worked_days_lines(self):
        lines_values = super()._get_new_worked_days_lines()
        if not lines_values:
            return lines_values

        struct_days_ids = self.struct_id.struct_days_ids.ids if self.struct_id and self.struct_id.struct_days_ids else []

        filtered_lines = [vals for vals in lines_values if vals[2].get('work_entry_type_id') not in struct_days_ids]
        return filtered_lines

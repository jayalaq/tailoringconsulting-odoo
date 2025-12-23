from lxml import etree

from odoo import api, fields, models


class HrLeave(models.Model):
    _inherit = 'hr.leave'

    hr_leave_id = fields.Many2one(
        comodel_name='hr.leave.allocation',
        string='Asignación'
    )
    from_date = fields.Date(
        string='Desde'
    )
    from_to = fields.Date(
        string='Hasta'
    )

    @api.model
    def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
        res = super(HrLeave, self).fields_view_get(
            view_id=view_id, view_type=view_type, toolbar=toolbar, submenu=submenu)
        if view_type == 'form':
            doc = etree.XML(res['arch'])
            for node in doc.xpath("//field[@name='hr_leave_id']"):
                leave_23_id = self.env.ref('holiday_process.hr_leave_type_23')
                leave_27_id = self.env.ref('automatic_leave_type.hr_leave_type_27')
                modifiers = f'{{"readonly": [["state", "not in", ["confirm"]]],' \
                            f' "invisible": [["holiday_status_id", "not in", [{leave_23_id.id}, {leave_27_id.id}]]]}}'
                node.set("modifiers", modifiers)
            res['arch'] = etree.tostring(doc, encoding='unicode')
        return res

    @api.onchange('holiday_status_id')
    def onchange_holiday_status_id(self):
        leave_23_id = self.env.ref('holiday_process.hr_leave_type_23')
        leave_27_id = self.env.ref('automatic_leave_type.hr_leave_type_27')
        leave_ids = [leave_27_id.id, leave_23_id.id]
        if self.holiday_status_id and self.holiday_status_id.id in leave_ids:
            self.hr_leave_id = False

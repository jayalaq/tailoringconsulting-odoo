from odoo import models, fields, api, _


class HrPayslip(models.Model):
    _inherit = 'hr.payslip'

    state = fields.Selection(selection_add=[('paid', u'Pagado')])
    state_move = fields.Char(compute='_compute_state_move')

    @api.depends('move_id', 'move_id.state')
    def _compute_state_move(self):
        for move in self:
            if move.move_id:
                move.state_move = move.move_id.state
            else:
                move.state_move = 'False'

    def action_move_id_post(self):
        for move in self.move_id:
            if move.state == 'draft':
                move.action_post()

    def action_move_id_draft(self):
        for move in self.move_id:
            move.button_draft()

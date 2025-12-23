import base64

from odoo import api, models

import logging

_logger = logging.getLogger(__name__)


class PosOrder(models.Model):
    _inherit = 'pos.order'

    @api.model
    def generate_pos_ui_report_action_value(self, move_id, report_action_ref):
        report_action_value = {'error': False, 'report': False}

        try:
            if isinstance(move_id, str):
                order_id = self.search([('pos_reference', '=', move_id)], limit=1)
                move_id = order_id.account_move.id
            
            report_id = self.env['ir.actions.report']._get_report(report_action_ref)
            if not move_id or not report_id:
                report_action_value['error'] = True
            else:
                report = self.env['ir.actions.report']._render_qweb_pdf(report_action_ref, [move_id])
                report_action_value['report'] = base64.b64encode(report[0])
        except Exception as error:
            report_action_value['error'] = True
            _logger.error("Error during report generation: %s") % str(error)

        return report_action_value

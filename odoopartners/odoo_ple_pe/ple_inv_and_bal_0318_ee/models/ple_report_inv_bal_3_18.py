import markupsafe

from odoo import models, fields, _
from odoo.tools import config


class PleReportInvBal(models.AbstractModel):
    _name = 'ple.report.inv.bal.3.18'
    _inherit = 'account.cash.flow.report.handler'
    _description = 'PLE Report Inv Bal 3.18'

    def open_wizard_txt_report_ple_3_18(self, options):
        new_wizard = self.env['wizard.report.txt.ple.3.18'].create({})
        view_id = self.env.ref('ple_inv_and_bal_0318_ee.view_wizard_report_txt_ple_3_18').id
        return {
            'type': 'ir.actions.act_window',
            'name': _('Generar TXT 3.18'),
            'view_mode': 'form',
            'res_model': 'wizard.report.txt.ple.3.18',
            'target': 'new',
            'res_id': new_wizard.id,
            'views': [[view_id, 'form']],
        }

    def _custom_options_initializer(self, report, options, previous_options=None):
        super()._custom_options_initializer(report, options, previous_options=previous_options)
        options['change_header'] = True
        options['buttons'].append({
            'name': _('EXPORTAR A TXT'),
            'sequence': 30,
            'action': 'open_wizard_txt_report_ple_3_18'
        })

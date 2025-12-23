from odoo import fields, models, api

class PleTransferCancel(models.Model):
    _name = 'ple.transfers.cancellations'
    _description = 'ple ransfers cancellations'

    ple_report_inv_val_seventeen_id = fields.Many2one(
        comodel_name='ple.report.inv.bal.seventeen',
        string='Reporte de Estado de Situación financiera'
    )
    transfers_cancellations_selection = fields.Selection(
        selection=[
            ('transfers', 'Transferencias'),
            ('cancellations', 'Cancelaciones'),
        ],
        string='Transferencias y cancelaciones '
    )
    trial_balances_catalog_id = fields.Many2one(
        string='Cuenta de balance de comprobación',
        comodel_name='trial.balances.catalog'
    )
    amount = fields.Char(
        string='Importe'
    )
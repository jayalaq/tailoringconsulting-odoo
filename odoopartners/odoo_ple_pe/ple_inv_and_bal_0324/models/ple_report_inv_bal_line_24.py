from odoo import models, fields


class PleInvBalLines24(models.Model):
    _name = 'ple.report.inv.bal.line.24'
    _description = 'Statements Comprehensive Income - Lines'
    _order = 'sequence desc'

    name = fields.Char(
        string='Periodo'
    )
    sequence = fields.Integer(
        string='Secuencia'
    )
    ple_report_inv_val_24_id = fields.Many2one(
        comodel_name='ple.report.inv.bal.24',
        string='Reporte de Estado de Resultados Integrales'
    )
    catalog_code = fields.Char(
        string='Código de catálogo'
    )
    financial_state_code = fields.Char(
        string='Código del Rubro del Estado Financiero'
    )
    eri_ple_id = fields.Many2one(
        string='Rubro ERI PLE',
        comodel_name='eeff.ple'
    )
    credit = fields.Char(
        string='Saldo del Rubro Contable'
    )
    state = fields.Char(
        string='Indica el estado de la operación'
    )
    account_ids = fields.Many2many(
        comodel_name='account.account',
        string='Cuentas',
        readonly=True
    )
    description = fields.Char(
        string='Descripción'
    )

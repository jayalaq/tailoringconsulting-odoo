from odoo import fields, models, _

class PleInvBalLines(models.Model):
    _name = 'ple.report.inv.bal.line.04'
    _description = 'Cuentas por cobrar - Líneas'
    _order = 'sequence desc'

    account = fields.Float(
        string="Nro Cuenta"
    )
    desc_account = fields.Char(
        string="Descripcion"
    )
    period = fields.Char(
        string="Periodo"
    )
    code_uo = fields.Char(
        string="Codigo unico de operacion"
    )
    correlative = fields.Char(
        string="Numero correlativo"
    )
    doc_type = fields.Char(
        string="Tipo de Documento"
    )
    doc_num = fields.Char(
        string="Numero de documento"
    )
    name_client = fields.Char(
        string="Apellido y Nombres, Den. o Raz. Social cliente"
    )
    date_ref = fields.Char(
        string="Fecha de Referencia"
    )
    mont = fields.Float(
        string="Monto de Cuenta por Cobrar"
    )
    status = fields.Char(
        string="Estado"
    )

    note = fields.Char(
        string="Nota"
    )
    valor = fields.Float(
        string='Valor'
    )

    sequence = fields.Float(
        string='Secuencia'
    )

    ple_report_inv_val_04_id = fields.Many2one(
        comodel_name='ple.report.inv.bal.04',
        string='Reporte de Estado de Situación financiera'
    )
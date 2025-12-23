from odoo import fields, models


class AccountJournal(models.Model):
    _inherit = 'account.journal'

    automated_sent = fields.Boolean(
        string='Envío Automático',
        help='''Si marca este campo, cuando una factura se publique se ejecutará de forma inmediata la acción de Envío de la factura electrónica. 
        Si no marca este campo, el envío se ejecutará con el Cron de envío de facturas, o al dar click en el botón "Enviar ahora".'''
    )






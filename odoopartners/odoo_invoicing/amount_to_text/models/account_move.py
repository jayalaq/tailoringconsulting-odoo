from odoo import models, api
from num2words import num2words


class AccountMove(models.Model):
    _inherit = 'account.move'

    @api.model
    def _amount_to_text(self):
        """
        Método que convierte el importe total de la factura (amount_total) a texto en español.

        :return: Cadena de texto que representa el importe total.
        :rtype: str
        """
        self.ensure_one()
        amount_i, amount_d = divmod(self.amount_total, 1)
        amount_d = int(round(amount_d * 100, 2))
        words = num2words(amount_i, lang='es')
        result = '%(words)s Y %(amount_d)02d/100 %(currency_name)s' % {
            'words': words,
            'amount_d': amount_d,
            'currency_name': self.currency_id.currency_unit_label,
        }
        return result.upper()

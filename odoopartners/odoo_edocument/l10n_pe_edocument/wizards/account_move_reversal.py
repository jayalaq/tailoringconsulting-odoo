from odoo import models, fields
from odoo.tools.translate import _


refund_reason_13 = ('13', 'Corrección del monto neto pendiente de pago y/o la(s) de vencimiento del \n pago único o de las cuotas y/o los montos '
                          'correspondientes a cada cuota , de ser el caso')


class AccountMoveReversal(models.TransientModel):
    _inherit = 'account.move.reversal'

    l10n_pe_edi_refund_reason = fields.Selection(selection_add=[refund_reason_13])

    def _prepare_default_reversal(self, move):
        values = super()._prepare_default_reversal(move)
        del values['ref']
        values.update({
            'ref': move.ref,
            'l10n_pe_edi_cancel_reason': _('Reversión de: %(move_name)s, %(reason)s',
                                           move_name=(move.name).replace(' ', ''), reason=self.reason)
            if self.reason
            else _('Reversión de: %s', move.name),
        })
        if 'l10n_latam_document_type_id' in values.keys() :
            if self.l10n_latam_document_number and '|' in self.l10n_latam_document_number:
                part_document = self.l10n_latam_document_number
                values.update({
                    'l10n_latam_document_type_id': int(part_document.split('|')[0]) if part_document.split('|')[0] else
                    values['l10n_latam_document_type_id']
                })
        return values

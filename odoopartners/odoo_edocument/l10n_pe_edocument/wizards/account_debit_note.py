from odoo import models


class AccountDebitNote(models.TransientModel):
    _inherit = 'account.debit.note'

    def _prepare_default_values(self, move):
        values = super()._prepare_default_values(move)
        del values['ref']
        values.update({
            'ref': move.ref,
            'l10n_pe_edi_cancel_reason': '%s, %s' % (
                (move.name).replace(' ', ''), self.reason) if self.reason else move.name,
        })
        return values

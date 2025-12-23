from odoo import fields, models


class AccountMoveReversal(models.TransientModel):
    _inherit = 'account.move.reversal'

    def reverse_moves(self, is_modify=False):
        action = super().reverse_moves()
        account_move = self.env['account.move'].browse(action['res_id'])
        if account_move.journal_id.automated_sent:
            account_move.edi_document_ids._process_documents_web_services(with_commit=False)
        return action

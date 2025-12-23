from odoo import fields, models

class AccountMove(models.Model):
    _inherit = 'account.move'

    def _post(self, soft=True):
        to_post = super()._post(soft)
        for move in self:
            if move.journal_id.automated_sent:
                docs = move.edi_document_ids.filtered(
                    lambda d: d.state in ('to_send', 'to_cancel') and d.blocking_level != 'error' and d.move_id.move_type in ['out_invoice', 'out_refund'])
                docs._process_documents_web_services(with_commit=False)
        return to_post
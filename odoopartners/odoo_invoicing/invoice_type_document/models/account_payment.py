from odoo import api, fields, models, _

class AccountPayment(models.Model):
    _inherit = "account.payment"

    @api.depends('move_id.line_ids.matched_debit_ids', 'move_id.line_ids.matched_credit_ids')
    def _compute_stat_buttons_from_reconciliation(self):
        super(AccountPayment, self)._compute_stat_buttons_from_reconciliation()
        for pay in self:
            serie_correlative = None
            document_type = None
            for move in pay.reconciled_invoice_ids:
                for line in move.line_ids:
                    if line.serie_correlative:
                        serie_correlative = line.serie_correlative
                    if line.l10n_latam_document_type_id:
                        document_type = line.l10n_latam_document_type_id
            for line in pay.move_id.line_ids:
                if line:
                    # Bloqueo explícito para evitar conflictos de concurrencia
                    self._cr.execute("SELECT id FROM account_move_line WHERE id=%s FOR UPDATE", (line.id,))
                    update_vals = {}
                    if document_type and line.l10n_latam_document_type_id != document_type:
                        update_vals['l10n_latam_document_type_id'] = document_type.id
                    if serie_correlative and line.serie_correlative != serie_correlative:
                        update_vals['serie_correlative'] = serie_correlative
                    if update_vals:
                        set_clause = ', '.join(f"{k}=%s" for k in update_vals)
                        params = list(update_vals.values()) + [line.id]
                        self._cr.execute(f"UPDATE account_move_line SET {set_clause} WHERE id=%s", params)
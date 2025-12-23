from odoo import api, fields, models, _


class AccountMove(models.Model):
    _inherit = 'account.move'

    serie_correlative = fields.Char(
        string='Serie-Correlativo',
        compute='_compute_serie_correlative_payment',
        store=True,
    )

    @api.depends('ref', 'name')
    def _compute_serie_correlative_payment(self):
        for move in self:
            if move.move_type in ['in_invoice', 'in_refund', 'in_receipt']:
                move.serie_correlative = move.ref
                (move.invoice_line_ids | move.line_ids).write({'serie_correlative': move.ref})
            elif move.move_type in ['out_invoice', 'out_refund', 'out_receipt'] and not move.journal_id.l10n_latam_use_documents and move.journal_id.type != 'sale':
                continue
            elif move.move_type in ['out_invoice', 'out_refund', 'out_receipt']:
                move.serie_correlative = move.name
                (move.invoice_line_ids | move.line_ids).write({'serie_correlative': move.name})
            elif move.move_type == 'entry':
                ids = [line.id for line in move.line_ids._all_reconciled_lines()]
                if ids:
                    # Bloqueo explícito para evitar conflictos de concurrencia
                    self.env.cr.execute("""
                                        SELECT id, l10n_latam_document_type_id, serie_correlative
                                        FROM account_move_line
                                        WHERE id in %s
                                          AND serie_correlative IS NOT NULL LIMIT 1
                                        """, [tuple(ids)])
                    row = self.env.cr.fetchone()
                    if row:
                        document_type, serie_correlative = row[1], row[2]
                        # Buscar líneas que no tengan document_type asignado
                        self.env.cr.execute("""
                                            SELECT id
                                            FROM account_move_line
                                            WHERE id in %s
                                              AND l10n_latam_document_type_id IS NULL
                                                FOR UPDATE
                                            """, [tuple(ids)])
                        ids_to_update = [r[0] for r in self.env.cr.fetchall()]
                        if ids_to_update:
                            self.env['account.move.line'].browse(ids_to_update).write({
                                'l10n_latam_document_type_id': document_type,
                                'serie_correlative': serie_correlative
                            })

    def _compute_name(self):
        super()._compute_name()
        for move in self:
            if move.move_type in ['out_invoice', 'out_refund', 'out_receipt']:
                for line in move.invoice_line_ids:
                    line.serie_correlative = move.name
                for line in move.line_ids:
                    line.serie_correlative = move.name






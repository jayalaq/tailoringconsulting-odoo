import base64

from odoo import api, models


class AccountEdiDocument(models.Model):
    _inherit = 'account.edi.document'

    def _process_job(self, job):
        super(AccountEdiDocument, self)._process_job(job)
        documents = self.env['account.edi.document']
        for doc in documents:
            if doc.state == 'sent':
                doc.write({
                    'error': False,
                    'blocking_level': False
                })

    @api.depends('move_id', 'error', 'state')
    def _compute_edi_content(self):
        """
        Override del método _compute_edi_content de addons/account_edi para manejar el resultado de
        _get_invoice_edi_content (enterprise/l10n_pe_edi) donde al momento de la implementacion retorna un markup.
        Se corrige para que se convierta en un flujo de bits.

        Observación:
        _get_invoice_edi_content llama a _generate_edi_invoice_bstr (enterprise/l10n_pe_edi) que renderiza el markup
        """
        for doc in self:
            res = b''
            if doc.state in ('to_send', 'to_cancel'):
                move = doc.move_id
                config_errors = doc.edi_format_id._check_move_configuration(move)
                if config_errors:
                    res = base64.b64encode('\n'.join(config_errors).encode('UTF-8'))
                else:
                    move_applicability = doc.edi_format_id._get_move_applicability(move)
                    if move_applicability and move_applicability.get('edi_content'):
                        res = self.handling_markkup_type_case(move_applicability['edi_content'](move))
            doc.edi_content = res

    def handling_markkup_type_case(self, file):
        return base64.b64encode(str(file).encode()) if type(file) != type(b'') else base64.b64encode(file)

from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    error_dialog = fields.Text(
        compute='_compute_error_dialog_partner',
        store=True,
        help='Campo usado para mostrar mensaje de alerta en el mismo formulario'
    )

    @api.model
    def _validate_length_vat(self, vat, doc_length, exact_length):
        if exact_length == 'exact':
            if len(vat) != doc_length:
                return '- El número de caracteres para el número de identificación debe ser: {doc_length}.\n'.format(doc_length=doc_length)

        elif exact_length == 'maximum':
            if len(vat) > doc_length:
                return '- El número de caracteres para el número de identificación deber ser como máximo: {doc_length}.\n'.format(doc_length=doc_length)

        return ''

    @api.model
    def _validate_structure_vat(self, vat, doc_type):
        if doc_type == 'other':
            return ''

        elif doc_type == 'numeric':
            if not vat.isdigit():
                return '- El número de identificación solo debe contener números.\n'

            digit_sum = sum(map(int, [character for character in vat if character.isdigit()]))
            if digit_sum == 0:
                return '- El número de identificación no puede contener solo ceros.\n'

        elif doc_type == 'alphanumeric':
            special_characters = '-°%&=~\\+?*^$()[]{}|@%#"/¡¿!:.,;'
            if any(char in special_characters for char in vat):
                return '- El número de identificación contiene caracteres no permitidos.\n'

        return ''

    @api.depends('l10n_latam_identification_type_id', 'vat')
    def _compute_error_dialog_partner(self):
        for partner in self:
            error_dialog = ''
            if partner.l10n_latam_identification_type_id and partner.vat:
                error_dialog += self._validate_length_vat(
                    partner.vat,
                    partner.l10n_latam_identification_type_id.doc_length,
                    partner.l10n_latam_identification_type_id.exact_length
                )
                error_dialog += self._validate_structure_vat(
                    partner.vat,
                    partner.l10n_latam_identification_type_id.doc_type
                )
            partner.error_dialog = error_dialog

    @api.onchange('vat')
    def _onchange_error_dialog_partner(self):
        if self.error_dialog:
            self.vat, self.error_dialog = False, self.error_dialog

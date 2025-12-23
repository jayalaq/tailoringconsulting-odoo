from odoo import api, models


class PosSession(models.Model):
    _inherit = 'pos.session'

    def _loader_params_l10n_latam_identification_type(self):
        search_params = {
            'search_params': {
                'fields': ['name'],
                'domain': [('active', '=', True)],
            }
        }
        additional_fields = ['doc_length', 'exact_length', 'doc_type', 'invoice_validation_document', 'is_vat']

        if hasattr(super(), '_loader_params_l10n_latam_identification_type'):
            original_params = super()._loader_params_l10n_latam_identification_type()
            for field in additional_fields:
                if field not in original_params['search_params']['fields']:
                    original_params['search_params']['fields'].append(field)
            return original_params
        else:
            search_params['search_params']['fields'].extend(additional_fields)
            return search_params

    def _get_pos_ui_l10n_latam_identification_type(self, params):
        return self.env['l10n_latam.identification.type'].search_read(**params['search_params'])

    @api.model
    def _pos_ui_models_to_load(self):
        models_to_load = super()._pos_ui_models_to_load()
        new_model = 'l10n_latam.identification.type'
        if new_model not in models_to_load:
            models_to_load.append(new_model)
        return models_to_load

    def _loader_params_res_partner(self):
        search_params = super()._loader_params_res_partner()
        if 'l10n_latam_identification_type_id' not in search_params['search_params']['fields']:
            search_params['search_params']['fields'].append('l10n_latam_identification_type_id')
        return search_params

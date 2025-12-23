from odoo import models

class AccountEdiXmlUBLPE(models.AbstractModel):
    _inherit = 'account.edi.xml.ubl_pe'

    def _get_invoice_line_vals(self, line, line_id, taxes_vals):
        vals = super()._get_invoice_line_vals(line, line_id, taxes_vals)
        vals['delivery_vals'] = self._get_delivery_line_vals(line)
        return vals

    def _get_delivery_line_vals(self, line):
        return {
            'origin_address': line.origin_address,
            'destiny_address': line.destiny_address,
            'service_detail': line.product_id.service_detail,
            'transportation_service': line.reference_value_transportation_service,
            'effective_load': line.reference_value_effective_load,
            'on_nominal_payload': line.reference_value_on_nominal_payload
        }

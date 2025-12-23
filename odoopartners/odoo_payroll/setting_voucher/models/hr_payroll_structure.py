from odoo import api, fields, models, _

class HrPayrollStructure(models.Model):
    _inherit = 'hr.payroll.structure'

    additional_certificate = fields.Selection(
        selection=lambda x: x.env['hr.payroll.structure']._get_additional_certificate(),
        string=u'Certificado adicional'
    )

    def get_additional_certificate_name(self):
        certificate_list = self._get_additional_certificate()
        data = list(filter(lambda x: x[0] == self[0].additional_certificate, certificate_list))
        if data:
            return data[0][1]
        else:
            return u'Reporte Adicional'

    @api.model
    def _get_additional_certificate(self):
        selection = []
        return selection

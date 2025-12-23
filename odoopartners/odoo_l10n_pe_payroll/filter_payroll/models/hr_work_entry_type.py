from odoo import fields, models

class HrWorkEntryType(models.Model):
    _inherit = 'hr.work.entry.type'

    unpaid = fields.Boolean(string='Es no Pagada?')
    is_social_benefits_license = fields.Boolean(string='¿Es Licencia para Benef. Sociales?')
    is_benefits_license_absence = fields.Boolean(string='¿Es Inasistencia para Benef. Sociales?')
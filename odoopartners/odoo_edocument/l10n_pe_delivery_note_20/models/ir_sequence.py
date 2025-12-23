from odoo import models, api


class IrSequence(models.Model):
    _inherit = 'ir.sequence'

    @api.depends('prefix')
    def _compute_display_name(self):
        for sequence in self:
            if self.env.context.get('default_sunat_sequence_id') and sequence.prefix:
                sequence.display_name = f'{sequence.prefix}'
            else:
                super()._compute_display_name()

    @api.model
    def _name_search(self, name, domain=None, operator='ilike', limit=None, order=None):
        if self.env.context.get('default_sunat_sequence_id'):
            domain = domain or []
            if name:
                domain = ['&', ('prefix', operator, name)] + domain
            return self._search(domain, limit=limit, order=order)
        return super()._name_search(name, domain, operator, limit, order)

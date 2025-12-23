from odoo import api, fields, models
from odoo.osv import expression

class TrialBalances(models.Model):
    _name = 'trial.balances.catalog'
    _description = '[3.17] Balance de comprobación'
    _order = 'sequence ASC'

    code = fields.Char(
        string='Código',
        required=True
    )
    name = fields.Char(
        string='Descripción',
        required=True
    )
    sequence = fields.Integer(
        string='Secuencia',
        required=True
    )

    @api.model
    def _name_search(self, name, args=None, operator='ilike', limit=100, order=None):
        args = args or []
        domain = []
        if name:
            domain = ['|', ('code', '=ilike', name.split(' ')[0] + '%'), ('name', operator, name)]
            if operator in expression.NEGATIVE_TERM_OPERATORS:
                domain = ['&', '!'] + domain[1:]
        return self._search(expression.AND([domain, args]), limit=limit, order=order)

    
    @api.depends('code','name')
    def _compute_display_name(self):
        for partner in self:
            partner.display_name = '[%s] %s' % (partner.code, partner.name)





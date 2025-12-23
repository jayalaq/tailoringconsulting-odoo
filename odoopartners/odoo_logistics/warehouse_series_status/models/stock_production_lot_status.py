from odoo import models, fields, api
from odoo.osv import expression


class ProductionLotStatus(models.Model):
    _name = 'stock.production.lot.status'
    _description = 'Status Stock Production Lot'

    code = fields.Char(string='Código', required=True)
    name = fields.Char(string='Nombre', required=True)

    @api.depends(lambda self: (self._rec_name,) if self._rec_name else ())
    def _compute_display_name(self):
        for record in self:
            record.display_name = f'{record.code}-{record.name}'

    @api.model
    def _name_search(self, name, args=None, operator='ilike', limit=100, order=None):
        args = args or []
        domain = []
        if name:
            domain = ['|', ('code', '=ilike', name.split(' ')[0] + '%'), ('name', operator, name)]
            if operator in expression.NEGATIVE_TERM_OPERATORS:
                domain = ['&', '!'] + domain[1:]
        return self._search(expression.AND([domain, args]), limit=limit, order=order)

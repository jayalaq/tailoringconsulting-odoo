
from odoo import models, fields

class StockMoveLine(models.Model):
    _inherit = 'stock.move.line'

    def _action_done(self):
        ml_dates = {}
        for ml in self:
            if ml.picking_id and ml.picking_id.date_done:
                ml_dates[ml.id] = ml.picking_id.date_done
        
        result = super(StockMoveLine, self)._action_done()
        
        for ml in self.exists():
            ml_date = ml_dates.get(ml.id) if ml.id in ml_dates else fields.Datetime.now()
            ml.write({
                'date': ml_date,
            })
        
        return result
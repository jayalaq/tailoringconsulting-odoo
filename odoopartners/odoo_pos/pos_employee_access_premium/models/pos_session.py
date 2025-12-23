from odoo import models


POS_ACCESS_FIELDS = [
    'pos_access_close',
    'pos_access_make_payments',
    'pos_access_make_refunds',
    'pos_access_make_discounts',
    'pos_access_change_price',
    'pos_access_delete_orders',
    'pos_access_delete_order_lines',
    'pos_access_decrease_quantity_order_lines',
    'pos_access_cash_in_out',
    'pos_access_product_information'
]


class PosSession(models.Model):
    _inherit = 'pos.session'

    def _loader_params_hr_employee(self):
        search_params = super()._loader_params_hr_employee()
        search_params['search_params']['fields'].extend(POS_ACCESS_FIELDS)
        return search_params

    def _loader_params_res_users(self):
        search_params = super()._loader_params_res_users()
        search_params['search_params']['fields'].extend(POS_ACCESS_FIELDS)
        return search_params

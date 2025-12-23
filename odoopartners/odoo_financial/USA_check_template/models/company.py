from odoo import models, fields


class Company(models.Model):
    _inherit = "res.company"

    # here, key has to be full xmlID(including the module name) of all the
    # new report actions that you have defined for check layout
    account_check_printing_layout = fields.Selection(selection_add=[
        ('USA_check_template.action_print_check_USA', 'Print Check USA - US'),
    ], ondelete={
        'USA_check_template.action_print_check_USA': 'set default',
    })
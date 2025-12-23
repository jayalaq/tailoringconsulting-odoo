from odoo import fields, models, api, _


class pos_config(models.Model):
	_inherit = 'pos.config'

	auto_invoice = fields.Boolean(string='Select default invoice') 
	stop_invoice_print = fields.Boolean(string='Disable auto print invoice') 
	

class ResConfigSettings(models.TransientModel):
	_inherit = 'res.config.settings'
	
	auto_invoice = fields.Boolean(related='pos_config_id.auto_invoice',readonly=False)
	stop_invoice_print = fields.Boolean(related='pos_config_id.stop_invoice_print',readonly=False)
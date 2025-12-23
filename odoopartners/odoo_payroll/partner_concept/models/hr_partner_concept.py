from odoo import fields, models


class HrPartnerConcept(models.Model):
    _name = 'hr.partner.concept'
    _description = 'Partner Concept'
    _rec_name = 'salary_rule_id'

    salary_rule_id = fields.Many2one(
        comodel_name='hr.salary.rule',
        string='Regla salarial'
    )
    partner_id = fields.Many2one(
        comodel_name='res.partner',
        string='Contacto',
        ondelete='restrict'
    )
    amount = fields.Float(
        string='Importe'
    )
    percentage = fields.Float(
        string='Porcentaje %'
    )
    is_debit = fields.Boolean(
        string='Debito'
    )
    is_credit = fields.Boolean(
        string='Crédito'
    )
    is_active = fields.Boolean(
        string='Activo'
    )
    start_date = fields.Date(
        string='Fecha Inicio'
    )
    end_date = fields.Date(
        string='Fecha Fin'
    )

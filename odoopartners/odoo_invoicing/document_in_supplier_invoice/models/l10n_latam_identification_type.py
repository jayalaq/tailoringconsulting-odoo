from odoo import models, fields, api


class L10nLatamDocumentType(models.Model):
    _inherit = 'l10n_latam.document.type'

    account_journal_id = fields.Many2one(
        'account.journal',
        string='Diario de Compras',
        help="""
            Debes escoger un diario de compras, solamente si este tipo de documento debe aparecer como opción
            en los comprobantes y rectificativos de proveedor. Si este documento no se utiliza en compras,
            debes dejar este campo vacío.
        """,
        domain="[('type', '=', 'purchase'), ('l10n_latam_use_documents', '=', False)]",
        company_dependent=True
    )

    account_journal_id_sale = fields.Many2one(
        comodel_name='account.journal',
        string='Diario de Ventas',
        help="""
            Debes escoger un diario de ventas, solamente si este tipo de documento debe aparecer como opción
            en los comprobantes y rectificativos de clientes. Si este documento no se utiliza en ventas,
            debes dejar este campo vacío.
        """,
        domain="['&', ('type', '=', 'sale'), ('l10n_latam_use_documents', '=', False)]",
        company_dependent=True
    )

    @api.model
    def _get_view(self, view_id=None, view_type='form', **options):
        arch, view = super()._get_view(view_id, view_type, **options)
        if view_type in ('form'):
            tags = [('field', 'account_journal_id'), ('field', 'account_journal_id_sale')]
            countries = [
                self.env.ref('base.pe'),  
                self.env.ref('base.cl'), 
                self.env.ref('base.ar'), 
                self.env.ref('base.ec') 
            ]
            arch, view = self.env['res.partner']._tags_invisible_per_country(arch, view, tags, countries)
        return arch, view


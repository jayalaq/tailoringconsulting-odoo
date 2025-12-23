from odoo import models, fields, api
from lxml import etree

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    def _l10n_pe_edi_get_qr(self):
        """ Retrieve the CDR's QR code. """
        try:
            self.ensure_one()
            result = super()._l10n_pe_edi_get_qr()
            if not result:
                return ''
                
            edi_filename = 'cdr-%s-09-%s.xml' % (
                self.company_id.vat,
                (self.l10n_latam_document_number or '').replace(' ', ''),
            )
            attachment = self.env['ir.attachment'].search([
                ('name', '=', edi_filename),
                ('res_id', '=', self.id),
                ('res_model', '=', self._name)], limit=1)
                
            if not attachment:
                return ''
                
            edi_attachment_str = attachment.raw
            edi_tree = etree.fromstring(edi_attachment_str)
            element = edi_tree.xpath('//cbc:DocumentDescription',
                                    namespaces={'cbc': 'urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2'})
                                    
            if not element:
                return ''
                
            return element[0].text
        except ValueError:
            return ''


class StockMoveLine(models.Model):
    _inherit = "stock.move.line"

    def _get_aggregated_product_weights(self, **kwargs):
        """ Returns a dictionary of products add weight (key = id+name+description+uom+weight) and corresponding values of interest."""
        res = super(StockMoveLine, self)._get_aggregated_product_quantities(**kwargs)
        for move_line in res.values():
            move_line["weight"] = move_line["product"].weight
        return res

class StockLocation(models.Model):
    _inherit = 'stock.location'

    direction_id = fields.Many2one(
        comodel_name='res.partner',
        string='Dirección',
        compute='_default_direction_id',
        inverse='_inverse_direction_id',
        default=False,
        store=True
    )

    @api.depends('warehouse_id.partner_id', 'active')
    def _default_direction_id(self):
        for record in self:
            if record.active and record.warehouse_id and record.warehouse_id.partner_id:
                record.direction_id = record.warehouse_id.partner_id
            else:
                record.direction_id = False

    def _inverse_direction_id(self):
        return
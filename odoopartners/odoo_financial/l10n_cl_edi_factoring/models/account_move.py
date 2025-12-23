# -*- coding: utf-8 -*-
from odoo import tools, fields, models, api, _
from odoo.exceptions import UserError
from lxml import etree
import logging
import urllib3
import base64


_logger = logging.getLogger(__name__)

try:
    from facturacion_electronica import facturacion_electronica as fe
except Exception as e:
    _logger.warning("Problema al cargar Facturación electrónica: %s" % str(e))


TIMEOUT = 30  # default timeout for all remote operations
pool = urllib3.PoolManager(timeout=TIMEOUT)

try:
    from suds.client import Client
except ImportError:
    _logger.warning('Cannot import suds')

SERVER_MODE = {
    'SIITEST': 'certificacion',
    'SIIDEMO': 'certificacion',
    'SII': 'produccion',
}

class CesionDTE(models.Model):
    _inherit = "account.move"

    cession_number = fields.Integer(
        copy=False,
        string='Cession Number',
        help='',
        default=1,
    )

    sworn_declaration = fields.Text(
        copy=False,
        string='Declaración Jurada',
        help='',
    )

    cession_partner_id = fields.Many2one(
        'res.partner',
        string="Cession Partner",
        help='',
    )


    sii_cesion_message = fields.Text(
        string='SII Message',
        copy=False,
    )

    l10n_cl_aec_file = fields.Many2one(
        'ir.attachment',
        string='AEC file',
        copy=False)

    l10n_cl_dte_cession_status = fields.Selection([
        ('not_sent', 'Pending To Be Sent'),
        ('ask_for_status', 'Ask For Status'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ], string='SII DTE Cession status', copy=False, tracking=True, help="""Status of sending the DTE to the SII:
    - Not sent: the DTE has not been sent to SII but it has created.
    - Ask For Status: The DTE is asking for its status to the SII.
    - Accepted: The DTE has been accepted by SII.
    - Rejected: The DTE has been rejected by SII.""")
    
    sii_xml_dte = fields.Text(string="SII XML DTE", copy=False, readonly=True, states={"draft": [("readonly", False)]},)

    @api.onchange('cession_partner_id')
    def set_declaracion(self):
        if self.cession_partner_id:
            sworn_declaration = f'''Se declara bajo juramento que {self.company_id.partner_id.name}, RUT {self.company_id.vat} \
ha puesto a disposicion del cesionario {self.cession_partner_id.name}, RUT {self.cession_partner_id.vat}, el o los documentos donde constan los recibos de las mercaderías entregadas o servicios prestados, \
entregados por parte del deudor de la factura {self.partner_id.commercial_partner_id.name}, RUT {self.partner_id.commercial_partner_id.vat}, de acuerdo a lo establecido en la Ley No. 19.983'''
            self.sworn_declaration = sworn_declaration

    def _get_xml(self):
        if self.l10n_cl_dte_file:
            xml = base64.b64decode(self.l10n_cl_dte_file.datas).decode("ISO-8859-1")
        return xml

    def _read_xml(self, mode="text", check=False):
        xml = (
            self._get_xml()
            .replace('<?xml version="1.0" encoding="ISO-8859-1"?>', "")
            .replace('<?xml version="1.0" encoding="ISO-8859-1" ?>', "")
        )
        if check:
            return xml
        xml = xml.replace('xmlns="http://www.sii.cl/SiiDte"', "")
        if mode == "etree":
            parser = etree.XMLParser(remove_blank_text=True)
            return etree.fromstring(xml, parser=parser)
        return xml

    def _get_dtes(self):
        xml = self._read_xml("etree")
        if xml.tag == "SetDTE":
            return xml.findall("DTE")
        envio = xml.find("SetDTE")
        if envio is None:
            if xml.tag == "DTE":
                return [xml]
            return []
        return envio.findall("DTE")
    
    def do_create_inv(self):
        dtes = self._get_dtes()
        for dte in dtes:
            try:
                documento = dte
                self.sii_xml_dte = "%s" % etree.tostring(documento).decode('ISO-8859-1')
            except:
                _logger.warning("Error DTE")
                
    def _crear_envio_cesion(self):
        datos = self._get_datos_empresa(self.company_id)
        datos['filename'] = "AEC_1"
        datos['Cesion'] = self._cesion()
        return datos
    
    def _get_datos_empresa(self, company_id):
        emisor = self._emisor()
        return {
            "Emisor": emisor,
            "firma_electronica": self.company_id._get_digital_signature(user_id=self.env.user.id).parametros_firma(),
        }

    def _emisor(self):
        Emisor = {}
        Emisor["RUTEmisor"] = self._l10n_cl_format_vat(self.company_id.vat)
        Emisor["RznSoc"] = self._l10n_cl_format_vat(self.company_id.name)
        Emisor["GiroEmis"] = self._format_length(self.company_id.l10n_cl_activity_description, 80)
        if self.company_id.phone:
            Emisor["Telefono"] = self._format_length(self.company_id.phone, 20)
        Emisor["CorreoEmisor"] = self.company_id.l10n_cl_dte_email
        Emisor["Actecos"] = self._actecos_emisor()
        dir_origen = self.company_id
        Emisor['DirOrigen'] = self._format_length(dir_origen.street + ' ' + (dir_origen.street2 or ''), 70)
        Emisor['CmnaOrigen'] = self.company_id.partner_id.city or ''
        Emisor["CiudadOrigen"] = self.company_id.city or ''
        Emisor["Modo"] = SERVER_MODE[self.company_id.l10n_cl_dte_service_provider]
        Emisor["NroResol"] = ''
        Emisor["FchResol"] = ''
        Emisor["ValorIva"] = 19
        return Emisor

    def _actecos_emisor(self):
        actecos = []
        for acteco in self.company_id.l10n_cl_company_activity_ids:
            actecos.append(acteco.code)
        return actecos
    
    def _cesion(self):
        data = {
            'ID': 'C%s%s' % (self.l10n_latam_document_type_id.code, int(self.l10n_latam_document_number)),
            'SeqCesion': self.cession_number,
            'IdDTE': self._id_dte(),
            'Cedente': self._cedente(),
            'Cesionario': self._cesionario(),
            'MontoCesion': self._monto_cesion(),
            'UltimoVencimiento': self.invoice_date.strftime('%Y-%m-%d'),
            'xml_dte': self.sii_xml_dte,
            'DeclaracionJurada': self.sworn_declaration,
        }
        return data
    
    def _cesionario(self):
        Receptor = {}
        Receptor['RUT'] = self._l10n_cl_format_vat(self.cession_partner_id.commercial_partner_id.vat)
        Receptor['RazonSocial'] = self.cession_partner_id.commercial_partner_id.name
        Receptor['Direccion'] = self.cession_partner_id.commercial_partner_id.street
        Receptor['eMail'] = self.cession_partner_id.commercial_partner_id.email
        return Receptor
   
    def _id_dte(self):
        IdDoc = {}
        IdDoc['TipoDTE'] = self.l10n_latam_document_type_id.code
        IdDoc['RUTEmisor'] = self._l10n_cl_format_vat(self.company_id.vat)
        IdDoc['RznSocReceptor'] = self.partner_id.commercial_partner_id.name
        IdDoc['RUTReceptor'] = self._l10n_cl_format_vat(self.partner_id.commercial_partner_id.vat)
        IdDoc['Folio'] = int(self.l10n_latam_document_number)
        IdDoc['FchEmis'] = self.invoice_date.strftime('%Y-%m-%d')
        IdDoc['MntTotal'] = self.currency_id.round(self.amount_total)
        return IdDoc

    def _cedente(self):
        Cedente = {
            'RUT': self._l10n_cl_format_vat(self.env.user.partner_id.vat),
            'Nombre': self.env.user.name,
            'Phono': self.env.user.partner_id.phone,
            'eMail': self.env.user.partner_id.email,
        }
        return Cedente

    def _monto_cesion(self):
        return self.currency_id.round(self.amount_total)

    def _l10n_cl_format_vat(self, value, with_zero=False):
        if not value or value in ['', 0]:
            value = 'CL666666666'
        if 'CL' in value:
            # argument is vat
            rut = value[:10] + '-' + value[10:]
            if not with_zero:
                rut = rut.replace('CL0', '')
            return rut.replace('CL', '')
        #  Argument is other
        return value.replace('.', '')
    
    def _format_length(self, text, text_len):
        return text and text[:text_len] or ''
        
    # This is The Heart
    def validate_cesion(self):
        if self.move_type == 'out_invoice':
            if not self.cession_partner_id.commercial_partner_id.email:
                raise UserError("Debe ingresar email Cesionario")
            try:
                self.do_create_inv()
                datos = self._crear_envio_cesion()
                result = fe.timbrar_y_enviar_cesion(datos)
                _logger.warning(result)

                dte_attachment = self.env['ir.attachment'].create({
                    'name': result['sii_send_filename'],
                    'res_model': 'account.move',
                    'res_id': self.id,
                    'type': 'binary',
                    'datas': base64.b64encode(result['sii_xml_request'].encode('ISO-8859-1', 'replace')),
                })

                self.l10n_cl_aec_file = dte_attachment.id
                self.sii_cesion_message
                self.message_post(body=_('DTE Cession has been sent to SII with response TRACKID: %s.') %
                                  result['sii_send_ident'])
            except Exception as e:
                self.message_post(body=_('Error: %s. No response from SII, Try again.' % str(e)))
            return
    
class Certificate(models.Model):
    _inherit = 'l10n_cl.certificate'

    def parametros_firma(self):
        return {
            "priv_key": self.private_key,
            "cert": self.certificate,
            "rut_firmante": self.subject_serial_number,
            "init_signature": False,
        }

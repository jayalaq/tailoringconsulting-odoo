import copy
from odoo import fields, models, api
from ..reports.report_inv_bal_08 import ReportInvBalEightExcel, ReportInvBalEightTxt
from dateutil.relativedelta import relativedelta
import base64
from odoo.exceptions import ValidationError
from collections import defaultdict
from copy import deepcopy


class PleInvBal108(models.Model):
    _name = 'ple.report.inv.bal.08'
    _description = 'Cuentas por Cobrar Diversas de Terceros y Relacionadas'
    _inherit = 'ple.report.base'

    line_ids = fields.One2many(
        comodel_name='ple.report.inv.bal.line.08',
        inverse_name='ple_report_inv_val_08_id',
        string='Líneas'
    )
    financial_statements_catalog = fields.Selection(
        selection=[
            ('01', 'SUPERINTENDENCIA DEL MERCADO DE VALORES - SECTOR DIVERSAS - INDIVIDUAL'),
            ('02', 'SUPERINTENDENCIA DEL MERCADO DE VALORES - SECTOR SEGUROS - INDIVIDUAL'),
            ('03', 'SUPERINTENDENCIA DEL MERCADO DE VALORES - SECTOR BANCOS Y FINANCIERAS - INDIVIDUAL'),
            ('04', 'SUPERINTENDENCIA DEL MERCADO DE VALORES - ADMINISTRADORAS DE FONDOS DE PENSIONES (AFP)'),
            ('05', 'SUPERINTENDENCIA DEL MERCADO DE VALORES - AGENTES DE INTERMEDIACIÓN'),
            ('06', 'SUPERINTENDENCIA DEL MERCADO DE VALORES - FONDOS DE INVERSIÓN'),
            ('07', 'SUPERINTENDENCIA DEL MERCADO DE VALORES - PATRIMONIO EN FIDEICOMISOS'),
            ('08', 'SUPERINTENDENCIA DEL MERCADO DE VALORES - ICLV'),
            ('09', 'OTROS NO CONSIDERADOS EN LOS ANTERIORES')
        ],
        string='Catálogo estados financieros',
        default='09',
        required=True
    )
    eeff_presentation_opportunity = fields.Selection(
        selection=[
            ('01', 'Al 31 de diciembre'),
            ('02', 'Al 31 de enero, por modificación del porcentaje'),
            ('03', 'Al 30 de junio, por modificación del coeficiente o porcentaje'),
            ('04',
             'Al último día del mes que sustentará la suspensión o modificación del coeficiente (distinto al 31 de enero o 30 de junio)'),
            ('05',
             'Al día anterior a la entrada en vigencia de la fusión, escisión y demás formas de reorganización de sociedades o emperesas o extinción '
             'de la persona jurídica'),
            ('06', 'A la fecha del balance de liquidación, cierre o cese definitivo del deudor tributario'),
            ('07', 'A la fecha de presentación para libre propósito')
        ],
        string='Oportunidad de presentación de EEFF',
        required=True
    )

    txt_filename = fields.Char(string='Filename .txt')
    txt_binary = fields.Binary(string='Reporte .TXT 3.8')

    pdf_filename = fields.Char(string='Filename .txt')
    pdf_binary = fields.Binary(string='Reporte .TXT 3.8')

    def name_get(self):
        return [(obj.id, '{} - {}'.format(obj.date_start.strftime('%d/%m/%Y'), obj.date_end.strftime('%d/%m/%Y'))) for
                obj in self]
    
    def _get_accounts(self):
        query = """
            SELECT
                aa.id
            FROM 
                account_account as aa
            WHERE 
                aa.ple_selection = 'investment_property_cost_3_8' OR aa.ple_selection = 'investment_property_provision_3_8';
        """
        try:
            self.env.cr.execute(query)
            accounts = self.env.cr.dictfetchall()
        except Exception as error:
            raise ValidationError(f'Error al ejecutar la queries, comunicar al administrador: \n {error}')
        
        return tuple(account['id'] for account in accounts)

    def _get_previous_document(self):
        document = self.env['ple.report.inv.bal.08'].search([
            ('company_id', '=', self.company_id.id),
            ('date_end', '<', self.date_start),
            ('state', 'in', ('load', 'closed'))], order='id desc', limit=1)
        
        if not document:
            return None
        previous_lines = self.env['ple.report.inv.bal.line.08'].search([
            ('ple_report_inv_val_08_id', '=', document.id)
        ])

        return previous_lines

    def _group_by_partner(self, lines):
        lines_data = [{
            'partner_id': line.partner_id if line.partner_id else False,
            'name': line.name,
            'total_title_costs': line.total_title_costs,
            'total_title_provision': line.total_title_provision,
            'line_id': line.id, 
            'type_document_transmitter': line.type_document_transmitter,
            'number_document_transmitter': line.number_document_transmitter,
            'transmitter_name': line.transmitter_name,
            'title_code': line.title_code,
            'title_unit_value': line.title_unit_value,
            'total_amount_value': line.total_amount_value,
        } for line in lines]
    
        grouped_lines = defaultdict(lambda: {
            'total_title_costs': 0.00,
            'total_title_provision': 0.00,
            'line': None
        })

        for line in lines_data:
            partner_id = line['partner_id']
            grouped = grouped_lines[partner_id]
            
            # Sumar las columnas
            grouped['total_title_costs'] += line['total_title_costs']
            grouped['total_title_provision'] += line['total_title_provision']
            
            # Mantener la línea más antigua
            if not grouped['line'] or line['name'] < grouped['line']['name']:
                grouped['line'] = line

        
        # Creamos nuevos registros o actualizamos los existentes sin modificar los originales
        result = []
        for partner_id, data in grouped_lines.items():
            line_data = data['line'].copy()  # Hacemos una copia del diccionario
            line_data.update({
                'total_title_costs': data['total_title_costs'],
                'total_title_provision': data['total_title_provision']
            })
            result.append(line_data)

        return result
    
    def _process_previous_lines(self, lines):
        grouped_lines = defaultdict(lambda: {
            'total_title_costs': 0.00,
            'total_title_provision': 0.00,
            'line': None
        })

        for line in lines:
            partner_id = line['partner_id']
            grouped = grouped_lines[partner_id]

            # Sumar las columnas
            grouped['total_title_costs'] += line['total_title_costs']
            grouped['total_title_provision'] += line['total_title_provision']

            # Mantener la línea más antigua
            if not grouped['line'] or line['name'] < grouped['line']['name']:
                grouped['line'] = line

        result = []
        for partner_id, data in grouped_lines.items():
            line = data['line']
            line['total_title_costs'] = data['total_title_costs']
            line['total_title_provision'] = data['total_title_provision']
            result.append(line)

        return result

    def _process_current_lines(self, lines):

        for line in lines:
            line.setdefault('state', '1')
            line.setdefault('total_amount_value', '0')
            if line['total_amount_value'] is None:
                line['total_amount_value'] = '0'

            if line['total_title_costs'] < 0:
                line['total_title_costs'] = 0.00
            else:
                line['total_title_provision'] = 0.00

            ple_selection = line['ple_selection']
            line['title_unit_value'] = 0.00 if ple_selection == 'investment_property_provision_3_8' else line['title_unit_value']
            line['total_amount_value'] = 0 if ple_selection == 'investment_property_provision_3_8' else line['total_amount_value']

        return lines


    def _get_current_lines(self, accounts):
        query = """
            SELECT
                '{date_self}' AS name,
                '{financial_statements_catalog}' as catalog_code,
                aml.id as camp_id,
                am.name as document_name,
                aml.ple_correlative as correlative,
                llit.l10n_pe_vat_code as type_document_transmitter,
                rp.vat as number_document_transmitter,
                rp.name as transmitter_name,
                aml.partner_id as partner_id,
                ai.title_code as title_code,
                ai.title_unit_value as title_unit_value,
                aa.ple_selection as ple_selection,
                ai.total_amount_value as total_amount_value,
                sum(aml.balance) as total_title_costs,
                sum(aml.balance) as total_title_provision,
                {ple_report_inv_val_id} as ple_report_inv_val_08_id

            -- QUERIES TO MATCH MULTI TABLES
                FROM account_move_line as aml
            --  TYPE JOIN   |  TABLE                               | MATCH
                LEFT JOIN    account_account as aa                  ON aml.account_id = aa.id
                LEFT JOIN    account_group as ag                    ON aa.group_id = ag.id
                LEFT JOIN    res_partner as rp                      ON aml.partner_id = rp.id
                LEFT JOIN    asset_intangible ai                    ON aml.asset_intangible_id = ai.id
                LEFT JOIN    account_move as am                     ON aml.move_id = am.id
                LEFT JOIN    l10n_latam_identification_type as llit ON llit.id = rp.l10n_latam_identification_type_id
            -- FILTER QUERIES 
                WHERE 
                    aml.date >= '{date_start}' AND 
                    aml.date <= '{date_end}' AND
                    aml.company_id = {company_id} AND
                    aml.account_id in {accounts} AND
                    am.state = '{state}'
                GROUP BY
                    number_document_transmitter, transmitter_name, correlative,
                    type_document_transmitter, document_name, title_code, ple_selection,
                    title_unit_value, total_amount_value, camp_id, aml.partner_id;
                """.format(
            company_id=self.company_id.id,
            date_start=self.date_start,
            date_end=self.date_end,
            state='posted',
            financial_statements_catalog=self.financial_statements_catalog,
            date_self=self.date_end.strftime('%Y%m%d'),
            accounts=accounts,
            ple_report_inv_val_id=self.id
        )

        try:
            self.env.cr.execute(query)
            current_lines = self.env.cr.dictfetchall()
            return current_lines

        except Exception as error:
            raise ValidationError(
                f'Error al ejecutar la queries, comunicar al administrador: \n {error}')
        
    def _working_with_previous_lines(self, previous_lines):
        previous_lines =  previous_lines.mapped(lambda line: {
            'name': self.date_end.strftime('%Y%m%d'),
            'catalog_code': line.catalog_code,
            'camp_id': line.camp_id,
            'document_name': line.document_name,
            'correlative': line.correlative,
            'type_document_transmitter': line.type_document_transmitter,
            'number_document_transmitter': line.number_document_transmitter,
            'transmitter_name': line.transmitter_name,
            'partner_id': line.partner_id,
            'title_code': line.title_code,
            'title_unit_value': line.title_unit_value,
            'ple_selection': line.ple_selection,
            'total_amount_value': line.total_amount_value,
            'total_title_costs': line.total_title_costs,
            'total_title_provision': line.total_title_provision,
            'state': line.state,
            'ple_report_inv_val_08_id': self.id
        })

        return self._process_previous_lines(previous_lines)

    def action_generate_excel(self):
        accounts = self._get_accounts()
        if not accounts:
            return
        
        previous_lines = self._get_previous_document()
        current_lines = self._get_current_lines(accounts=accounts)

        if previous_lines:
            previous_lines_data = self._working_with_previous_lines(previous_lines)
            lines = previous_lines_data + self._process_current_lines(current_lines)
        else:
            lines = self._process_current_lines(current_lines)
        self.env['ple.report.inv.bal.line.08'].create(lines)
        report_xls = ReportInvBalEightExcel(self, lines)
        report_txt = ReportInvBalEightTxt(self, lines)

        values_content_xls = report_xls.get_content()
        values_content_txt = report_txt.get_content()

        data = {
            'txt_binary': base64.b64encode(values_content_txt.encode() or '\n'.encode()),
            'txt_filename': report_txt.get_filename(),
            'error_dialog': 'No hay contenido para presentar en el registro de ventas electrónicos de este periodo.' if not values_content_txt else False,
            'xls_binary': base64.b64encode(values_content_xls),
            'xls_filename': report_xls.get_filename(),
            'date_ple': fields.Date.today(),
            'state': 'load'
        }

        self.write(data)

        for rec in self:
            report_name = "ple_inv_and_bal_0308.action_print_status_finance"
            pdf = self.env.ref(report_name)._render_qweb_pdf('ple_inv_and_bal_0308.print_status_finance', self.id)[0]
            rec.pdf_binary = base64.encodebytes(pdf)
            year, month, day = self.date_end.strftime('%Y/%m/%d').split('/')
            rec.pdf_filename = f'Libro_Inversiones Mobiliarias_{year}{month}.pdf'

    def action_close(self):
        self.write({'state': 'closed'})

    def action_rollback(self):
        self.write({'state': 'draft'})
        self.write({
            'txt_binary': False,
            'txt_filename': False,
            'xls_binary': False,
            'xls_filename': False,
            'pdf_binary': False,
            'pdf_filename': False,
            'line_final_ids': False,
            'line_ids': False,
        })


class PleInvBalLines(models.Model):
    _name = 'ple.report.inv.bal.line.08'
    _description = 'Cuentas por cobrar - Líneas'
    _order = 'name desc'

    ple_report_inv_val_08_id = fields.Many2one(
        comodel_name='ple.report.inv.bal.08',
        string='Reporte de Estado de Situación financiera'
    )

    name = fields.Char(string='Periodo')
    partner_id = fields.Integer(string="Id del partner_id")
    camp_id = fields.Char()
    state = fields.Char(string='Indica el estado de la operación')
    catalog_code = fields.Char(string='Código de catálogo')
    document_name = fields.Char(string='Nombre')
    correlative = fields.Char(string='Correlative')
    type_document_transmitter = fields.Integer(
        string="Tipo de documento del deudor"
    )
    number_document_transmitter = fields.Char(
        string="Numero de documento del transmisor"
    )
    transmitter_name = fields.Char(
        string="Razon social"
    )
    title_code = fields.Char(
        string="Código de titulo"
    )
    ple_selection = fields.Char(
        string="Ple selection"
    )
    title_unit_value = fields.Integer(
        string="Valor unitario del titulo"
    )
    total_amount_value = fields.Char(
        string="Valor del monto total",
    )
    total_title_costs = fields.Float(
        string="Costo del monto total",
        digits=(16, 2)
    )
    total_title_provision = fields.Float(
        string="Provision total del titulo",
        digits=(16, 2)
    )
    transmitter_name = fields.Char(
        string="Razón social"
    )
    free_camp = fields.Char(
        string="Campo libre"
    )

 
class PleInvBal1One(models.Model):
    _inherit = 'ple.report.inv.bal.one'

    m2o_ple_report_inv_bal_08 = fields.Many2one('ple.report.inv.bal.08')
    txt_filename_8 = fields.Char(string='Filaname_08 .txt')
    txt_binary_8 = fields.Binary(string='Reporte .TXT 3.8')
    pdf_filename_8 = fields.Char(string='Filaname_08 .pdf')
    pdf_binary_8 = fields.Binary(string='Reporte .PDF 3.8')
    xls_filename_8 = fields.Char(string='Filaname_08 Excel')
    xls_binary_8 = fields.Binary(string='Reporte Excel')

    def create_book_08(self):
        self.m2o_ple_report_inv_bal_08 = self.env['ple.report.inv.bal.08'].create(
            {
                'company_id': self.company_id.id,
                'date_start': self.date_start,
                'date_end': self.date_end,
                'state_send': self.state_send,
                'date_ple': self.date_ple,
                'financial_statements_catalog': self.financial_statements_catalog,
                'eeff_presentation_opportunity': self.eeff_presentation_opportunity,
            }
        )

        self.m2o_ple_report_inv_bal_08.action_generate_excel()

        self.xls_filename_8 = self.m2o_ple_report_inv_bal_08.xls_filename
        self.xls_binary_8 = self.m2o_ple_report_inv_bal_08.xls_binary
        self.txt_filename_8 = self.m2o_ple_report_inv_bal_08.txt_filename
        self.txt_binary_8 = self.m2o_ple_report_inv_bal_08.txt_binary
        self.pdf_filename_8 = self.m2o_ple_report_inv_bal_08.pdf_filename
        self.pdf_binary_8 = self.m2o_ple_report_inv_bal_08.pdf_binary

    def action_generate_excel(self):
        self.create_book_08()
        super(PleInvBal1One, self).action_generate_excel()

    def action_rollback(self):
        self.m2o_ple_report_inv_bal_08.unlink()
        super(PleInvBal1One, self).action_rollback()

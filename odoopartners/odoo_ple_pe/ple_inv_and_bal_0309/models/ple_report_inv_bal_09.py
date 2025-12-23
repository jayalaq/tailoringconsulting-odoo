from collections import defaultdict
from odoo import fields, models, api
from ..reports.report_inv_bal_09 import ReportInvBalNineExcel, ReportInvBalNineTxt

import base64
from odoo.exceptions import ValidationError
from itertools import groupby


class PleInvBal09(models.Model):
    _name = 'ple.report.inv.bal.09'
    _inherit = 'ple.report.base'

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

    line_ids_309 = fields.One2many(
        comodel_name='ple.report.inv.bal.line.09',
        inverse_name='ple_report_inv_val_09_id',
        string='Líneas'
    )

    xls_filename_309 = fields.Char(string='Filaname Excel 3.9')
    xls_binary_309 = fields.Binary(string='Reporte Excel')
    txt_filename_309 = fields.Char(string='Filename .txt')
    txt_binary_309 = fields.Binary(string='Reporte .TXT 3.9')
    pdf_filename_309 = fields.Char(string='Filename .txt')
    pdf_binary_309 = fields.Binary(string='Reporte .TXT 3.9')
    
    @api.depends('date_start', 'date_end')
    def _compute_display_name(self):
        for rec in self:
            if rec.date_start and rec.date_end:
                rec.display_name = '%s - %s' % (rec.date_start.strftime('%d/%m/%Y'), rec.date_end.strftime('%d/%m/%Y'))
            else:
                rec.display_name = ''

    def action_generate_excel(self):
        # self.line_ids_309.unlink()
        data = self.generate_data_report_309()

        report_xls = ReportInvBalNineExcel(self, data)
        report_txt = ReportInvBalNineTxt(self, data)

        values_content_xls = report_xls.get_content()
        values_content_txt = report_txt.get_content()

        data = {
            'txt_binary_309': base64.b64encode(values_content_txt.encode() or '\n'.encode()),
            'txt_filename_309': report_txt.get_filename(),
            'error_dialog': 'No hay contenido para presentar en el registro de ventas electrónicos de este periodo.' if not values_content_txt else False,
            'xls_binary_309': base64.b64encode(values_content_xls),
            'xls_filename_309': report_xls.get_filename(),
            'date_ple': fields.Date.today(),
            'state': 'load'
        }

        self.write(data)

        for rec in self:
            report_name = "ple_inv_and_bal_0309.action_print_status_finance"
            pdf = self.env.ref(report_name)._render_qweb_pdf(
                'ple_inv_and_bal_0309.print_status_finance', rec.id)[0]
            rec.pdf_binary_309 = base64.encodebytes(pdf)
            year, month, day = self.date_end.strftime('%Y/%m/%d').split('/')
            rec.pdf_filename_309 = f"Libro_Activos_Intangibles_{year}{month}.pdf"

    def _group_for_pdf(self, lines):
        lines_data = [{
            'ple_selection': line.ple_selection,
            'operation_date': line.operation_date,
            'name_aml': line.name_aml,
            'balance': line.balance,
            'balance_amortization_xls': line.balance_amortization_xls,
            'name': line.name,
        } for line in lines]
    
        group = defaultdict(lambda: {'balance': 0, 'balance_amortization_xls': 0})

        for item in lines_data:
            group[item['name_aml']]['balance'] += item['balance']
            group[item['name_aml']]['balance_amortization_xls'] += item['balance_amortization_xls']
            group[item['name_aml']]['operation_date'] = item['operation_date']
        result = [{'name_aml': key, **value} for key, value in group.items()]
        
        return result

    def _get_previous_document(self):
        document = self.env['ple.report.inv.bal.09'].search([
            ('company_id', '=', self.company_id.id),
            ('date_end', '<', self.date_start),
            ('state', 'in', ('load', 'closed'))
        ], order = 'id desc', limit=1)

        if not document:
            return None
        
        previous_lines = self.env['ple.report.inv.bal.line.09'].search([
            ('ple_report_inv_val_09_id', '=', document.id)
        ])

        lines = previous_lines.mapped(lambda line: {
            'aml_name': line.name_aml,
            'balance_amortization_xls': line.balance_amortization_xls
        })


        return lines
    
    def _calculate_amortization(self, aml_name, lines):
        sum_amortization = 0

        if lines is None:
            return 0.00

        for line in lines:
            if aml_name == line['aml_name']:
                sum_amortization += line['balance_amortization_xls']
        
        return sum_amortization

    def generate_data_report_309(self):

        query = """
       CREATE OR REPLACE FUNCTION calculate_balance_AMORTIZATION(date_start TIMESTAMP,
                                                                asset_itg INTEGER,
                                                                am_id INTEGER,
                                                                OUT amount_pe FLOAT) AS $$
        BEGIN
        SELECT  sum(aml.balance) into amount_pe
               -- QUERIES TO MATCH MULTI TABLES
                  FROM account_move_line as aml
                  LEFT JOIN account_move am ON  aml.move_id=am.id
                  LEFT JOIN account_account aa on aml.account_id=aa.id
                  LEFT JOIN account_group  ag on aa.group_id=ag.id
              -- FILTER QUERIES 
                  WHERE 
                  aml.asset_intangible_id = asset_itg
                  AND aml.date < date_start
                  AND ag.code_prefix_start = '39'
                  AND aml.balance < 0
                  AND am.state = 'posted'
                  AND am.id = am_id;
        END;
        $$ 
        LANGUAGE plpgsql;
        
        
        SELECT
        am.name as name_s,
        aml.ple_correlative as ple_correlative,
        aa.ple_selection as ple_selection,
        aa.code as code_account,
        aml.name as name_aml,
        ai.operation_date as operation_date,
        round(sum(aml.balance), 2) as balance,
        ag.code_prefix_start as code_prefix_start,
        round(COALESCE(calculate_balance_AMORTIZATION('{date_end}',aml.asset_intangible_id,am.id)::NUMERIC,0), 2) as balance_amortization,
        round(COALESCE(calculate_balance_AMORTIZATION('{date_start}',aml.asset_intangible_id,am.id)::NUMERIC,0), 2) as balance_amortization_xls,
        {ple_report_inv_val_id} as ple_report_inv_val_09_id
        
        -- QUERIES TO MATCH MULTI TABLES
        FROM  ACCOUNT_MOVE_LINE aml
         --  TYPE JOIN   |  TABLE               | MATCH
        LEFT JOIN ACCOUNT_MOVE am            ON am.id=aml.move_id
        LEFT JOIN account_account AA         ON aml.account_id = aa.id
        LEFT JOIN asset_intangible AI    ON  aml.asset_intangible_id=ai.id
        LEFT JOIN account_group ag          ON AA.group_id=ag.id
        -- FILTER QUERIES 
        WHERE 
        aa.ple_selection in ('investment_active_intangible_3_9','investment_active_intangible_deprecated_3_9')
        and aa.company_id ='{company_id}'
        and (('{date_start}' <=aml.date) or   (aml.date < '{date_start}' and ag.code_prefix_start='34'))
        and aml.date <= '{date_end}'
        and am.state = 'posted'
      
       
        GROUP BY 
        am.id,aml.id, aa.id,ai.operation_date,ag.code_prefix_start
       """.format(
            company_id=self.company_id.id,
            date_start=self.date_start,
            date_end=self.date_end,
            state='posted',
            financial_statements_catalog=self.financial_statements_catalog,
            date_self=self.date_end.strftime('%Y%m%d'),
            ple_report_inv_val_id=self.id
        )

        lines_previous = self._get_previous_document()
        try:
            self.env.cr.execute(query)
            values = self.env.cr.dictfetchall()

            for line in values:
                pool_amortization = self._calculate_amortization(line['name_aml'], lines_previous)
                if line['balance'] < 0 and line['ple_selection'] == 'investment_active_intangible_deprecated_3_9':
                    line.update(
                        {
                            'balance_amortization_xls': line['balance'],
                            'balance': 0.00,
                        })
                elif line['balance'] > 0 and pool_amortization != 0:
                    line.update({
                        'balance_amortization_xls': pool_amortization
                    })
                    
                line.setdefault('state', '1')
                period = self.date_end.strftime('%Y%m%d')
                line.setdefault('date', period)
                
                print(f"balance_amortization_xls: {line['balance_amortization_xls']}")

            self.env['ple.report.inv.bal.line.09'].create(values)

        except Exception as error:
            raise ValidationError(
                f'Error al ejecutar la queries, comunicar al administrador: \n {error}')

        return values

    def action_close(self):
        self.write({'state': 'closed'})

    def action_rollback(self):
        self.write({'state': 'draft'})
        self.write({
            'txt_binary_309': False,
            'txt_filename_309': False,
            'xls_binary_309': False,
            'xls_filename_309': False,
            'pdf_binary_309': False,
            'pdf_filename_309': False,
            'line_ids_309': False,
        })

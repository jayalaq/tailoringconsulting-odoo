import base64

from dateutil.relativedelta import relativedelta
from odoo.exceptions import ValidationError

from odoo import fields, models, api
from ..reports.report_inv_bal_excel import ReportInvBalExcel
from ..reports.report_inv_bal_txt import ReportInvBalTxt


def calculate_standard_price(line: dict) -> dict:
    """
    Calcular el precio estándar para un artículo de línea dado.

    Esta función calcula el precio estándar basado en la cantidad del producto disponible.
        - Si la cantidad es mayor que cero, el precio estándar se calcula como el total dividido por la cantidad.
        - Si la cantidad es cero, el precio estándar se establece como el total.
        - Si la cantidad es negativa, el precio estándar se calcula como el valor absoluto del total dividido por la cantidad.

    Params:
        line (dict): Un diccionario que contiene los detalles del producto. Las claves esperadas son:
            - 'quantity_product_hand' (float): La cantidad del producto disponible.
            - 'total' (float): El valor total del producto.

    Returns:
        dict: El diccionario del artículo de línea actualizado con la clave 'standard_price' añadida o actualizada.
    """
    if line['quantity_product_hand'] > 0:
        line.setdefault('standard_price', line['total'] / line['quantity_product_hand'])
    elif line['quantity_product_hand'] == 0:
        line.setdefault('standard_price', line['total'])
    else:
        line.setdefault('standard_price', abs(line['total'] / line['quantity_product_hand']))

    return line


class PleReportInvBal07(models.Model):
    _name = 'ple.report.inv.bal.07'
    _description = 'Estado de Situación financiera'
    _inherit = 'ple.report.base'

    # line_initial_ids
    # line_final_ids
    line_ids = fields.One2many(
        comodel_name='ple.report.inv.bal.line.07',
        inverse_name='ple_report_inv_val_07_id',
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
    txt_binary = fields.Binary(string='Reporte .TXT 3.7')
    pdf_filename = fields.Char(string='Filename .pdf')
    pdf_binary = fields.Binary(string='Reporte .PDF 3.7')

    @api.depends('date_start', 'date_end')
    def _compute_display_name(self):
        for rec in self:
            if rec.date_start and rec.date_end:
                rec.display_name = '%s - %s' % (rec.date_start.strftime('%d/%m/%Y'), rec.date_end.strftime('%d/%m/%Y'))
            else:
                rec.display_name = ''

    def action_generate_excel(self):
        """Genera el archivo Excel y otros formatos."""
        accounts = self._get_accounts()
        if not accounts:
            return
        
        document, previous_lines, date_condition = self._get_previous_document()
        current_lines = self._get_current_lines(accounts, date_condition)

        if previous_lines:
            previous_lines_data = self._map_previous_lines(previous_lines)
            lines = self._combine_previous_and_current_lines(previous_lines_data, current_lines)
        else:
            lines = self._validate_and_enrich_lines(current_lines)

        lines = self._calculate_period(lines)
        self.env['ple.report.inv.bal.line.07'].create(lines)
        self._generate_files(lines)

    def _get_accounts(self):
        """
        Obtiene cuentas con prefijos de código 20 y 21.

        Esta función ejecuta una consulta SQL para obtener las cuentas que tienen un prefijo de código 20 o 21.
        Si no se encuentran cuentas, se escribe un mensaje de error en el registro actual.

        Returns:
            tuple: Una tupla con los IDs de las cuentas encontradas.
        """
        query = """
            SELECT
                aa.id 
            FROM 
                account_account aa
            INNER JOIN account_group ag ON aa.group_id = ag.id
            WHERE ag.code_prefix_start IN ('20','21')
        """
        try:
            self.env.cr.execute(query)
            accounts_values = self.env.cr.dictfetchall()
        except Exception as error:
            raise ValidationError(f'Error al ejecutar la query, comunicar al administrador:\n{error}')

        if not accounts_values:
            self.write({
                'error_dialog': 'No hay cuentas configuradas con prefijo de código 20 o 21'
            })
            return tuple()

        return tuple(account['id'] for account in accounts_values)

    def _get_previous_document(self):
        """
        Obtiene el documento anterior y sus líneas.

        Esta función busca el documento anterior basado en la fecha de finalización, la compañía y el estado.
        Si no se encuentra ningún documento, devuelve None, False y una condición de fecha.
        Si se encuentra un documento, obtiene las líneas del documento anterior y calcula la condición de fecha para las líneas actuales.

        Returns:
            tuple: Una tupla que contiene el documento anterior, las líneas del documento anterior y la condición de fecha.
        """
        document = self.env['ple.report.inv.bal.07'].search([
            ('date_end', '<', self.date_end),
            ('company_id', '=', self.company_id.id),
            ('state', 'in', ('load', 'closed')),
        ], order='date_end desc', limit=1)

        if not document:
            return None, False, f"aml.date <= '{self.date_end}'"

        previous_lines = self.env['ple.report.inv.bal.line.07'].search([
            ('ple_report_inv_val_07_id', '=', document.id)
        ])
        
        start_date = document.date_end + relativedelta(days=1)
        date_condition = f"aml.date BETWEEN '{start_date}' AND '{self.date_end}'"
        
        return document, previous_lines, date_condition
    
    def _get_current_lines(self, accounts, date_condition) -> list[dict]:
        """
        Obtiene las líneas actuales para el libro.

        Esta función ejecuta una consulta SQL para obtener las líneas actuales de productos basadas en las cuentas y la condición de fecha proporcionadas.

        Params:
            accounts (tuple): Una tupla con los IDs de las cuentas.
            date_condition (str): Una cadena que representa la condición de fecha para la consulta SQL.

        Returns:
            list[dict]: Una lista de diccionarios que representan las líneas actuales de productos.
        """
        query = """
            SELECT
                pp.id AS product_id,
                -- periodo
                pt.stock_catalog AS stock_catalog,
                pt.stock_type AS stock_type,
                pt.default_code AS default_code,
                pt.unspsc_code_id AS code_catalog_used,
                puc.code AS unspsc_code,
                pt.name AS product_description,
                uu.l10n_pe_edi_measure_unit_code AS product_udm,
                -- property_cost_method
                SUM(aml.quantity) AS quantity_product_hand,
                -- standard_price
                SUM(aml.balance) AS total
            FROM
                account_move_line aml
            LEFT JOIN product_product AS pp ON aml.product_id = pp.id
            LEFT JOIN product_template AS pt ON pp.product_tmpl_id = pt.id
            LEFT JOIN product_unspsc_code AS puc ON pt.unspsc_code_id = puc.id
            LEFT JOIN uom_uom AS uu ON pt.uom_id = uu.id
            LEFT JOIN account_move AS am ON aml.move_id = am.id
            WHERE
                {date_condition}
                AND aml.company_id = {company_id}
                AND aml.account_id IN {accounts}
                AND am.state = 'posted'
            GROUP BY
                pp.id,
                pt.stock_catalog,
                pt.stock_type,
                pt.default_code,
                pt.unspsc_code_id,
                puc.code,
                pt.name,
                uu.l10n_pe_edi_measure_unit_code;
        """.format(
            date_condition=date_condition,
            company_id=self.company_id.id,
            accounts=accounts
        )

        try:
            self.env.cr.execute(query)
            current_lines = self.env.cr.dictfetchall()
        except Exception as error:
            raise ValidationError(f'Error al ejecutar la query, comunicar al administrador:\n{error}')
        
        return current_lines

    def _map_previous_lines(self, previous_lines) -> list[dict]:
        """
        Mapea las líneas anteriores a diccionarios y le agregamos el id del reporte actual.

        Esta función toma una lista de líneas anteriores y las convierte en una lista de diccionarios con los campos necesarios.

        Params:
            previous_lines (list): Lista de objetos de líneas anteriores.

        Returns:
            list[dict]: Lista de diccionarios que representan las líneas anteriores mapeadas.
        """
        return previous_lines.mapped(lambda line: {
            'product_id': line.product_id,
            'stock_catalog': line.stock_catalog,
            'stock_type': line.stock_type,
            'default_code': line.default_code,
            'code_catalog_used': line.code_catalog_used,
            'unspsc_code': line.unspsc_code,
            'product_description': line.product_description,
            'product_udm': line.product_udm,
            'quantity_product_hand': line.quantity_product_hand,
            'standard_price': line.standard_price,
            'property_cost_method': line.property_cost_method,
            'total': line.total,
            'ple_report_inv_val_07_id': self.id
        })
    
    def _combine_previous_and_current_lines(self, previous_lines, current_lines):
        """
        Combina las líneas anteriores y actuales de productos.
        Debemos calcular el balance anterior y unirlo a las lineas de la consulta actual, pero el balance anterior ya tiene
        validadas las lineas, asi que solo debemos sumar las cantidades y totales de las lineas actuales a las anteriores.

        Params:
            previous_lines (list): Lista de diccionarios que representan las líneas de productos.
            current_lines (list): Lista de diccionarios que representan las líneas de productos actuales.

        Returns:
            list: Lista combinada de diccionarios con las líneas de productos.
        """
        current_lines_map = {line['product_id']: line for line in current_lines}
        combined_lines = []

        for pre_line in previous_lines:
            current_line = current_lines_map.pop(pre_line['product_id'], None)
            if current_line:
                pre_line['quantity_product_hand'] += current_line['quantity_product_hand']
                pre_line['total'] += current_line['total']
                pre_line = calculate_standard_price(pre_line)
            combined_lines.append(pre_line)

        remaining_lines = list(current_lines_map.values())
        validated_lines = self._validate_and_enrich_lines(remaining_lines)

        return combined_lines + validated_lines
    
    def _validate_and_enrich_lines(self, lines: list[dict]) -> list[dict]:
        """
        Valida y enriquece las líneas con datos adicionales por defecto.

        Params:
            lines (list[dict]): Lista de diccionarios que representan las líneas de productos.

        Returns:
            list[dict]: Lista de diccionarios con las líneas de productos validadas y enriquecidas.
        """
        for line_07 in lines:

            line_07['ple_report_inv_val_07_id'] = self.id
            # estas validaciones son independientes de si la linea tiene un producto o no
            line_07['code_catalog_used'] = '1' if line_07.get('code_catalog_used') else ''
            line_07['unspsc_code'] = (line_07.get('unspsc_code') or '')[:128]

            # si tiene un producto entonces hacemos las validaciones
            if line_07['product_id']:
                line_07['stock_catalog'] = line_07.get('stock_catalog') or ''
                line_07['stock_type'] = line_07.get('stock_type') or ''
                line_07['default_code'] = (line_07.get('default_code') or '')[:24]

                # obtener la descripción del producto
                product_description = line_07.get('product_description')
                if product_description and isinstance(product_description, dict):
                    line_07['product_description'] = product_description.get('es_PE', product_description['en_US'])[:80]
                elif product_description and isinstance(product_description, str):
                    line_07['product_description'] = product_description[:80]
                else:
                    line_07['product_description'] = ''

                line_07['product_udm'] = (line_07.get('product_udm')) or ''

                # obtener metodo de costo del producto
                product = self.env['product.product'].browse(line_07['product_id'])
                property_cost_method = product.categ_id.property_cost_method

                match property_cost_method:
                    case 'standard':
                        line_07.setdefault('property_cost_method', '9')
                    case 'average':
                        line_07.setdefault('property_cost_method', '1')
                    case 'fifo':
                        line_07.setdefault('property_cost_method', '2')
                    case _:
                        line_07.setdefault('property_cost_method', '')
            else:
                # cuando la linea no tiene un producto se debe completar con estos campos
                line_07['stock_catalog'] = '1'
                line_07['stock_type'] = '01'
                line_07['default_code'] = 'SINREF'
                line_07['product_description'] = 'SINPRODUCT'
                line_07['product_udm'] = 'NIU'
                line_07['property_cost_method'] = '1'

            # esto es para evitar divisiones por cero y valores negativos (independiente de si la linea tiene un producto o no)
            calculate_standard_price(line_07)
        return lines

    def _calculate_period(self, lines):
        for line in lines:
            line['period'] = f"{self.date_end.year}{self.date_end.month:02d}{self.date_end.day:02d}"
        return lines

    def _generate_files(self, list_data):
        """Genera los archivos TXT y XLS."""
        txt_report = ReportInvBalTxt(self, list_data)
        xls_report = ReportInvBalExcel(self, list_data)

        values_content_txt = txt_report.get_content().encode()
        values_content_xls = xls_report.get_content()

        self.write({
            'txt_binary': base64.b64encode(values_content_txt or '\n'.encode()),
            'txt_filename': txt_report.get_filename(),
            'error_dialog': 'No hay contenido para presentar en el registro de ventas electrónicos de este periodo.' if not values_content_txt else False,
            'xls_binary': base64.b64encode(values_content_xls),
            'xls_filename': xls_report.get_filename(),
            'date_ple': fields.Date.today(),
            'state': 'load',
        })

        for rec in self:
            report_name = 'ple_inv_and_bal_0307.action_print_status_finance'
            pdf = self.env.ref(report_name)._render_qweb_pdf('ple_inv_and_bal_0307.print_status_finance', self.id)[0]
            rec.pdf_binary = base64.encodebytes(pdf)
            year, month, day = self.date_end.strftime('%Y/%m/%d').split('/')
            rec.pdf_filename = f'Libro_Mercaderias y Productos Terminados_{year}{month}.pdf'

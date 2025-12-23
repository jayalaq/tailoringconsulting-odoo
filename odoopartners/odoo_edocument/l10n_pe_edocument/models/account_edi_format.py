from requests.exceptions import ConnectionError, HTTPError, ReadTimeout, InvalidSchema
from zeep.wsse.username import UsernameToken
from zeep import Client, Settings
from zeep.exceptions import Fault
from zeep.transports import Transport
from lxml import etree, objectify
from odoo import _, api, models
import zipfile
from io import BytesIO
import base64
from odoo.tools import html_escape

DEFAULT_BLOCKING_LEVEL = 'error'


class AccountEdiFormat(models.Model):
    _inherit = 'account.edi.format'

    @staticmethod
    def _l10n_pe_edi_request_raise_for_status(request_response):
        """Almacena raises class:`HTTPError`, si ocurre un error."""

        http_error_msg = ''
        if 400 <= request_response.status_code < 500:
            http_error_msg = 'Client Error: %s ' % request_response.content
        elif 500 <= request_response.status_code < 600:
            http_error_msg = 'Server Error: %s ' % request_response.content

        if http_error_msg:
            raise HTTPError(http_error_msg, response=request_response)

    @api.model
    def _l10n_pe_edi_get_general_error_messages(self):
        """ Agrega mensaje de error """
        res = super(AccountEdiFormat, self)._l10n_pe_edi_get_general_error_messages()
        res['L10NPE12'] = 'No se ha podido establecer la conexión.'
        return res

    def _l10n_pe_edi_get_ose_credentials(self, company):
        """ Credenciales OSE """
        self.ensure_one()
        res = {'fault_ns': 'soap-env'}
        if company.l10n_pe_edi_test_env:
            res.update({
                'wsdl': company.l10n_pe_edi_provider_ose_test_wsdl,
                'token': UsernameToken('{}MODDATOS'.format(company.vat), 'MODDATOS'),
            })
        else:
            res.update({
                'wsdl': company.l10n_pe_edi_provider_ose_prod_wsdl,
                'token': UsernameToken('{}{}'.format(company.vat, company.sudo().l10n_pe_edi_provider_username), company.sudo().l10n_pe_edi_provider_password),
            })
        return res

    def remove_existing_edi_attachments(self, invoice, edi_filename):
        """
        Elimina archivos adjuntos existentes con el mismo nombre de archivo EDI
        para evitar duplicados.
        """
        existing_attachments = self.env['ir.attachment'].search([
            ('res_model', '=', invoice._name),
            ('res_id', '=', invoice.id),
            ('name', '=', '%s.zip' % edi_filename)
        ])

        if existing_attachments:
            existing_attachments.unlink()

    def l10n_pe_edi_attachment_xml(self, invoice, edi_filename, zip_edi_str):
        """ Genera archivo xml """
        self.remove_existing_edi_attachments(invoice, edi_filename)
        attachment_id = self.env['ir.attachment'].create({
            'res_model': invoice._name,
            'res_id': invoice.id,
            'type': 'binary',
            'name': '%s.zip' % edi_filename,
            'datas': base64.encodebytes(zip_edi_str),
            'mimetype': 'application/zip'
        })
        message = _("EL documento EDI tiene un formato incorrecto, revisar el .zip")
        invoice.with_context(no_new_invoice=True).message_post(
            body=message,
            attachment_ids=[attachment_id.id],
        )

    @api.model
    def _l10n_pe_edi_validate_error_code_cdr(self, error_code):
        """
        Verifica el código devuelto por el CDR, si es un código validado o un código de error
        :param error_code: Valor devuelto por el CDR
        :return:
        """
        list_error_codes = [
            '0100', '0109', '0111', '0127', '0151', '0154', '0155', '0156', '0157', '0158', '0159', '0160', '0161',
            '0306', '1001', '1003', '1004', '1007', '1008', '1032', '1033', '1034', '1035', '1036', '1037', '1038',
            '1049', '1050', '1051', '1055', '1056', '1057', '1058', '1062', '1063', '1065', '1067', '1068', '1069',
            '1078', '1079', '1080', '1083', '2010', '2011', '2014', '2015', '2016', '2017', '2018', '2021', '2022',
            '2023', '2024', '2025', '2026', '2027', '2028', '2031', '2033', '2036', '2037', '2040', '2041', '2048',
            '2052', '2054', '2062', '2064', '2065', '2068', '2070', '2071', '2072', '2073', '2074', '2075', '2076',
            '2077', '2078', '2079', '2080', '2081', '2082', '2083', '2084', '2085', '2086', '2087', '2088', '2089',
            '2090', '2091', '2092', '2093', '2094', '2095', '2097', '2098', '2099', '2100', '2101', '2105', '2108',
            '2116', '2117', '2119', '2120', '2121', '2128', '2133', '2134', '2135', '2136', '2137', '2138', '2139',
            '2172', '2188', '2199', '2204', '2205', '2207', '2208', '2209', '2218', '2219', '2220', '2223', '2228',
            '2229', '2236', '2238', '2239', '2241', '2242', '2251', '2254', '2255', '2256', '2257', '2261', '2263',
            '2268', '2269', '2271', '2275', '2276', '2278', '2282', '2287', '2288', '2301', '2305', '2306', '2307',
            '2308', '2309', '2310', '2311', '2312', '2313', '2315', '2323', '2324', '2325', '2326', '2329', '2335',
            '2337', '2344', '2346', '2348', '2355', '2357', '2364', '2365', '2367', '2369', '2370', '2371', '2373',
            '2375', '2377', '2398', '2399', '2400', '2409', '2410', '2411', '2416', '2426', '2450', '2451', '2452',
            '2453', '2454', '2455', '2456', '2457', '2458', '2459', '2460', '2461', '2462', '2463', '2464', '2465',
            '2466', '2467', '2468', '2469', '2470', '2503', '2505', '2509', '2511', '2512', '2513', '2514', '2516',
            '2517', '2520', '2521', '2522', '2524', '2529', '2548', '2554', '2555', '2581', '2582', '2583', '2591',
            '2592', '2593', '2594', '2595', '2596', '2597', '2600', '2601', '2602', '2603', '2604', '2605', '2607',
            '2608', '2609', '2610', '2612', '2617', '2618', '2619', '2620', '2621', '2622', '2623', '2625', '2626',
            '2628', '2629', '2635', '2636', '2637', '2638', '2640', '2641', '2642', '2643', '2644', '2650', '2659',
            '2661', '2663', '2667', '2668', '2669', '2671', '2678', '2679', '2680', '2685', '2687', '2690', '2691',
            '2692', '2693', '2694', '2696', '2697', '2698', '2699', '2700', '2702', '2705', '2707', '2711', '2713',
            '2715', '2716', '2719', '2721', '2722', '2723', '2724', '2728', '2730', '2732', '2733', '2734', '2735',
            '2736', '2737', '2740', '2742', '2746', '2748', '2749', '2752', '2753', '2755', '2756', '2757', '2758',
            '2759', '2760', '2761', '2762', '2764', '2765', '2766', '2767', '2768', '2769', '2771', '2772', '2773',
            '2775', '2776', '2777', '2778', '2779', '2780', '2781', '2788', '2792', '2797', '2798', '2800', '2801',
            '2802', '2807', '2808', '2822', '2823', '2825', '2845', '2846', '2848', '2861', '2862', '2863', '2875',
            '2880', '2881', '2883', '2884', '2885', '2891', '2892', '2893', '2895', '2896', '2897', '2898', '2899',
            '2920', '2936', '2949', '2954', '2955', '2956', '2957', '2958', '2961', '2964', '2968', '2985', '2986',
            '2987', '2989', '2990', '2992', '2993', '2996', '2999', '3000', '3003', '3006', '3007', '3014', '3016',
            '3019', '3020', '3021', '3024', '3025', '3026', '3027', '3029', '3030', '3031', '3033', '3034', '3035',
            '3037', '3050', '3051', '3052', '3053', '3059', '3063', '3064', '3065', '3067', '3068', '3071', '3072',
            '3073', '3074', '3088', '3089', '3090', '3092', '3093', '3094', '3095', '3096', '3097', '3098', '3099',
            '3101', '3102', '3103', '3104', '3105', '3107', '3108', '3109', '3110', '3111', '3114', '3115', '3116',
            '3117', '3118', '3119', '3120', '3122', '3123', '3124', '3125', '3126', '3127', '3128', '3129', '3130',
            '3131', '3132', '3133', '3134', '3135', '3136', '3137', '3138', '3139', '3140', '3141', '3142', '3143',
            '3144', '3145', '3146', '3147', '3148', '3149', '3150', '3151', '3152', '3153', '3154', '3155', '3156',
            '3157', '3158', '3159', '3160', '3161', '3162', '3163', '3164', '3165', '3166', '3167', '3168', '3169',
            '3170', '3171', '3172', '3173', '3174', '3175', '3181', '3194', '3195', '3202', '3203', '3204', '3205',
            '3206', '3207', '3208', '3209', '3210', '3211', '3212', '3213', '3214', '3215', '3216', '3217', '3218',
            '3219', '3220', '3221', '3223', '3224', '3230', '3233', '3234', '3236', '3237', '3238', '3239', '3240',
            '3241', '3242', '3243', '3244', '3245', '3246', '3247', '3248', '3249', '3250', '3251', '3252', '3253',
            '3254', '3255', '3256', '3257', '3259', '3260', '3261', '3262', '3263', '3264', '3265', '3266', '3267',
            '3269', '3270', '3271', '3272', '3273', '3274', '3275', '3276', '3277', '3278', '3279', '3280', '3281',
            '3282', '3283', '3284', '3285', '3286', '3287', '3288', '3289', '3290', '3291', '3292', '3293', '3294',
            '3295', '3296', '3297', '3298', '3299', '3300', '3301', '3302', '3303', '3304', '3305', '3306', '3307',
            '3308', '3309', '3310', '3311', '3312', '3313', '3314', '3315', '4000', '4043', '4050', '4051', '4052',
            '4053', '4126', '4127', '4128', '4135', '4136', '4154', '4155', '4157', '4158', '4159', '4160', '4161',
            '4162', '4163', '4164', '4165', '4167', '4170', '4172', '4173', '4174', '4176', '4179', '4181', '4184',
            '4189', '4204', '4249', '4251', '4252', '4253', '4255', '4256', '4257', '4273', '4274', '4275', '4276',
            '4277', '4278', '4286', '4290', '4294', '4298', '4299', '4303', '4309', '4311'
        ]
        return True if error_code in list_error_codes else False

    @api.model
    def _l10n_pe_edi_decode_cdr(self, cdr_str):
        self.ensure_one()
        res = super(AccountEdiFormat, self)._l10n_pe_edi_decode_cdr(cdr_str)

        # Comprueba si el CDR tiene un error fatal
        if not res.get('error'):
            # Obtiene la respuesta de la aplicación (de forma predeterminada es una matriz de bytes en formato de string)
            try:
                cdr_tree = etree.fromstring(cdr_str)
                application_response = cdr_tree.find('.//{*}applicationResponse')
                if application_response is not None:
                    # Convierte de str a base64
                    cdr_bytes = base64.b64decode(application_response.text)
                    # Obtiene xml de la respuesta zip
                    xml_response = ""
                    with zipfile.ZipFile(BytesIO(cdr_bytes)) as z:
                        for archive in z.namelist():
                            if "xml" in archive:
                                xml_response = z.read(archive)
                    cdr_tree = etree.fromstring(xml_response)
                    cdr_response = cdr_tree.find('.//{*}DocumentResponse/{*}Response')
                    if cdr_response is not None:
                        code = cdr_response[1].text
                        message = cdr_response[2].text
                        if self._l10n_pe_edi_validate_error_code_cdr(code):
                            error_messages_map = self._l10n_pe_edi_get_cdr_error_messages()
                            error_message = '%s<br/><br/><b>%s</b><br/>%s|%s' % (
                                error_messages_map.get(code, _("We got an error response from the OSE. ")),
                                _('Original message:'),
                                html_escape(code),
                                html_escape(message),
                            )
                            return {'error': error_message}
            except Exception as error:
                error_message = '%s<br/><br/><b>%s</b><br/>%s<br/>%s' % (
                    'Error en el procesamiento del CDR', _('Original message:'),
                    'Por favor, revise si la información fue enviada en SUNAT. En todo caso, comunicar al adminstrador.', error)
                return {'error': error_message}
        return res

    # FUNCIONES OSE
    def _l10n_pe_edi_cancel_invoices_step_1_sunat_digiflow_common(self, company, invoices, void_filename, void_str, credentials):
        self.ensure_one()

        void_tree = objectify.fromstring(void_str)
        void_tree = company.l10n_pe_edi_certificate_id.sudo()._sign(void_tree)
        void_str = etree.tostring(void_tree, xml_declaration=True, encoding='ISO-8859-1')
        zip_void_str = self._l10n_pe_edi_zip_edi_document([('%s.xml' % void_filename, void_str)])
        transport = Transport(operation_timeout=15, timeout=15)

        try:
            settings = Settings(raw_response=True)
            client = Client(
                wsdl=credentials['wsdl'],
                wsse=credentials['token'],
                settings=settings,
                transport=transport,
            )
            result = client.service.sendSummary('%s.zip' % void_filename, zip_void_str)
            self._l10n_pe_edi_request_raise_for_status(result)
        except Fault:
            return {'error': self._l10n_pe_edi_get_general_error_messages()['L10NPE07'], 'blocking_level': 'warning'}
        except (InvalidSchema, KeyError):
            return {'error': self._l10n_pe_edi_get_general_error_messages()['L10NPE08'], 'blocking_level': 'error'}
        except HTTPError as http_error:
            return {'error': http_error, 'blocking_level': 'warning'}
        cdr_str = result.content
        cdr_decoded = self._l10n_pe_edi_decode_cdr(cdr_str)
        cdr_number = cdr_decoded.get('number')
        if cdr_decoded.get('error'):
            return {'error': cdr_decoded['error'], 'blocking_level': 'error'}
        return {'success': True, 'xml_document': void_str, 'cdr': cdr_str, 'cdr_number': cdr_number}

    def _l10n_pe_edi_sign_invoices_sunat_digiflow_common(self, invoice, edi_filename, edi_str, credentials):
        self.ensure_one()

        if not invoice.company_id.l10n_pe_edi_certificate_id:
            return {'error': _("No valid certificate found for %s company.", invoice.company_id.display_name)}

        # Firma el documento.
        edi_tree = objectify.fromstring(edi_str)
        edi_tree = invoice.company_id.l10n_pe_edi_certificate_id.sudo()._sign(edi_tree)
        error = self.env['ir.attachment']._l10n_pe_edi_check_with_xsd(edi_tree, invoice.l10n_latam_document_type_id.code)
        if error:
            return {'error': _('XSD validation failed: %s', error), 'blocking_level': 'error'}
        edi_str = etree.tostring(edi_tree, xml_declaration=True, encoding='ISO-8859-1')
        transport = Transport(operation_timeout=15, timeout=15)
        zip_edi_str = self._l10n_pe_edi_zip_edi_document([('%s.xml' % edi_filename, edi_str)])
        err_txt = {}
        try:
            settings = Settings(raw_response=True)
            client = Client(
                wsdl=credentials['wsdl'],
                wsse=credentials['token'],
                settings=settings,
                transport=transport
            )
            result = client.service.sendBill('%s.zip' % edi_filename, zip_edi_str)
            self._l10n_pe_edi_request_raise_for_status(result)
        except Fault as sf:
            msj = sf.detail.find('message').text if sf.detail is not None else False
            err_txt = {'error': msj if msj else sf.message, 'blocking_level': 'error'}
        except ConnectionError:
            err_txt = {'error': self._l10n_pe_edi_get_general_error_messages()['L10NPE08'], 'blocking_level': 'warning'}
        except HTTPError as http_error:
            err_txt = {'error': http_error, 'blocking_level': 'warning'}
        except ReadTimeout:
            err_txt = {'error': self._l10n_pe_edi_get_general_error_messages()['L10NPE12'], 'blocking_level': 'warning'}
        if err_txt:
            self.l10n_pe_edi_attachment_xml(invoice, edi_filename, zip_edi_str)
            return err_txt

        cdr_bytes = result.content
        application_response = etree.fromstring(cdr_bytes).xpath('//applicationResponse')
        if not application_response:
            unzipped_cdr = False
        else:
            unzipped_cdr = self._l10n_pe_edi_unzip_edi_document(base64.b64decode(application_response[0].text))

        cdr_decoded = self._l10n_pe_edi_decode_cdr(cdr_bytes)
        if cdr_decoded.get('error'):
            self.l10n_pe_edi_attachment_xml(invoice, edi_filename, zip_edi_str)
            return {'error': cdr_decoded['error'], 'blocking_level': 'error'}

        return {'success': True, 'xml_document': edi_str, 'cdr': unzipped_cdr}

    def _l10n_pe_edi_sign_invoices_ose(self, invoice, edi_filename, edi_str):
        credentials = self._l10n_pe_edi_get_ose_credentials(invoice.company_id)
        return self._l10n_pe_edi_sign_invoices_sunat_digiflow_common(invoice, edi_filename, edi_str, credentials)

    def _l10n_pe_edi_cancel_invoices_step_1_ose(self, company, invoices, void_filename, void_str):
        credentials = self._l10n_pe_edi_get_ose_credentials(company)
        return self._l10n_pe_edi_cancel_invoices_step_1_sunat_digiflow_common(company, invoices, void_filename, void_str, credentials)

    def _l10n_pe_edi_cancel_invoices_step_2_ose(self, company, edi_values, cdr_number):
        credentials = self._l10n_pe_edi_get_ose_credentials(company)
        return self._l10n_pe_edi_cancel_invoices_step_2_sunat_digiflow_common(company, edi_values, cdr_number, credentials)

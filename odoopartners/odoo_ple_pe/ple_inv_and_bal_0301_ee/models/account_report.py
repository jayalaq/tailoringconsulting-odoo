import io
from itertools import groupby

import markupsafe

from odoo import fields, models, _


class AccountReport(models.Model):
    _inherit = "account.report"

    allow_txt_generation = fields.Selection(
        selection_add=[('01', '3.1 Estado de situación financiera')]
    )

    def open_wizard_txt_report_ple_3_1(self, options):
        self.ensure_one()
        new_wizard = self.env['wizard.report.txt.ple.3.1'].create({'report_id': self.id})
        view_id = self.env.ref('ple_inv_and_bal_0301_ee.wizard_report_txt_ple_3_1_view_form').id
        return {
            'type': 'ir.actions.act_window',
            'name': _('Generar TXT 3.1'),
            'view_mode': 'form',
            'res_model': 'wizard.report.txt.ple.3.1',
            'target': 'new',
            'res_id': new_wizard.id,
            'views': [[view_id, 'form']],
        }

    def get_options(self, previous_options=None):
        options = super(AccountReport, self).get_options(previous_options)
        if self.allow_txt_generation == '01':
            options['change_header'] = True
            options['buttons'].append({
                'name': _('EXPORTAR A TXT'),
                'sequence': 30,
                'action': 'open_wizard_txt_report_ple_3_1'
            })
        return options

    def export_to_pdf(self, options):
        if self.allow_txt_generation != '01':
            return super(AccountReport, self).export_to_pdf(options)

        base_url = self.env['ir.config_parameter'].sudo().get_param('report.url') or self.env[
            'ir.config_parameter'].sudo().get_param('web.base.url')
        rcontext = {
            'mode': 'print',
            'base_url': base_url,
            'company': self.env.company,
        }

        print_options = self.get_options(previous_options={**options, 'export_mode': 'print'})
        if print_options['sections']:
            reports_to_print = self.env['account.report'].browse(
                [section['id'] for section in print_options['sections']])
        else:
            reports_to_print = self

        reports_options = []
        bodies = []
        for report in reports_to_print:
            reports_options.append(
                report.get_options(previous_options={**print_options, 'selected_section_id': report.id}))
            report_options = report.get_options(previous_options={**print_options, 'selected_section_id': report.id})
            body = report._get_pdf_export_html(
                report_options,
                report._filter_out_folded_children(report._get_lines(report_options)),
                additional_context={'base_url': base_url}
            )
            body_string = str(body)
            special_header = \
                self.env['ir.actions.report']._render_qweb_html('ple_inv_and_bal_0301_ee.action_report_header_ple_3_1',
                                                                self.id)[0]
            body_string = body_string.replace(
                '<div t-att-class="\'o_content \' + options[\'css_custom_class\']">',
                '<div t-att-class="\'o_content \' + options[\'css_custom_class\']">' + special_header.decode()
            )
            body = markupsafe.Markup(body_string)
            bodies.append(body)

        grouped_reports_by_format = groupby(
            zip(reports_to_print, reports_options),
            key=lambda report: len(report[1]['columns']) > 5
        )

        footer = self.env['ir.actions.report']._render_template("account_reports.internal_layout", values=rcontext)
        footer = self.env['ir.actions.report']._render_template("web.minimal_layout", values=dict(rcontext, subst=True,
                                                                                                  body=markupsafe.Markup(
                                                                                                      footer.decode())))
        action_report = self.env['ir.actions.report']
        files_stream = []
        for is_landscape, reports_with_options in grouped_reports_by_format:
            bodies = []

            for report, report_options in reports_with_options:
                bodies.append(report._get_pdf_export_html(
                    report_options,
                    report._filter_out_folded_children(report._get_lines(report_options)),
                    additional_context={'base_url': base_url}
                ))

            files_stream.append(
                io.BytesIO(action_report._run_wkhtmltopdf(
                    bodies,
                    footer=footer.decode(),
                    landscape=is_landscape or self._context.get('force_landscape_printing'),
                    specific_paperformat_args={
                        'data-report-margin-top': 10,
                        'data-report-header-spacing': 10,
                        'data-report-margin-bottom': 15,
                    }
                )
                ))

        if len(files_stream) > 1:
            result_stream = action_report._merge_pdfs(files_stream)
            result = result_stream.getvalue()
            # Close the different stream
            result_stream.close()
            for file_stream in files_stream:
                file_stream.close()
        else:
            result = files_stream[0].read()

        return {
            'file_name': self.get_default_report_filename(options, 'pdf'),
            'file_content': result,
            'file_type': 'pdf',
        }

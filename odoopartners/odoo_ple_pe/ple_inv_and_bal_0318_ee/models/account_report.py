import markupsafe
import io
from odoo import models, fields, _
from odoo.tools import config
from itertools import groupby

class AccountReport(models.Model):
    _inherit = 'account.report'
    
    is_ple_report_inv_bal_3_18 = fields.Boolean(string='Is PLE Report Inv Bal 3.18', default=False)

    def export_to_pdf(self, options):
        if not self.is_ple_report_inv_bal_3_18:
            return super(AccountReport, self).export_to_pdf(options)
        
        if not config['test_enable']:
            self = self.with_context(commit_assetsbundle=True)

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
            self.env['ir.actions.report']._render_qweb_html('ple_inv_and_bal_0318_ee.action_report_header_ple_3_18',
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
import base64
import copy
import datetime
import dateutil.relativedelta as relativedelta
import logging
import functools
from werkzeug import urls
from odoo import _, api, fields, models, tools

_logger = logging.getLogger(__name__)
try:
    # Se usa un entorno jinja2 para renderizar plantillas mako.
    # Tener en cuenta que la representación no cubre toda la sintaxis mako, en particular
    # no se aceptan declaraciones arbitrarias de Python y no se permiten todas las expresiones:
    # solo se puede acceder a los atributos "públicos" (que no comienzan con '_') de los objetos.
    # Esto se hace a propósito: evita la ejecución incidental o maliciosa de
    # código Python que puede romper la seguridad del servidor.
    from jinja2.sandbox import SandboxedEnvironment

    mako_template_env = SandboxedEnvironment(
        block_start_string="<%",
        block_end_string="%>",
        variable_start_string="${",
        variable_end_string="}",
        comment_start_string="<%doc>",
        comment_end_string="</%doc>",
        line_statement_prefix="%",
        line_comment_prefix="##",
        trim_blocks=True,  # no generar nueva línea después de los bloques
        autoescape=True,  # Escaping automático XML/HTML
    )
    mako_template_env.globals.update({
        'str': str,
        'quote': urls.url_quote,
        'urlencode': urls.url_encode,
        'datetime': datetime,
        'len': len,
        'abs': abs,
        'min': min,
        'max': max,
        'sum': sum,
        'filter': filter,
        'reduce': functools.reduce,
        'map': map,
        'round': round,

        # es una clase de estilo antiguo y no se puede crear una instancia
        # directamente dentro de una expresión jinja2 expression, por lo que aparentemente
        # se necesita un "proxy" lambda.
        'relativedelta': lambda *a, **kw: relativedelta.relativedelta(*a, **kw),
    })
    mako_safe_template_env = copy.copy(mako_template_env)
    mako_safe_template_env.autoescape = False
except ImportError:
    _logger.warning("jinja2 not available, templating features will not work!")


class HrContract(models.Model):
    _inherit = 'hr.contract'

    service_duration = fields.Char(
        string=u'Duración de contrato',
        compute='compute_service_duration',
        store=True
    )
    additional_info = fields.Text(
        string='Información adicional para contrato'
    )
    contract_template_id = fields.Many2one(
        comodel_name='mail.template',
        string='Usar plantilla para contrato',
        default=lambda self: self.env.ref('contract_formats.template_hr_contract', raise_if_not_found=False)
    )
    contract_name = fields.Char(
        string='Nombre de contrato - PDF'
    )
    contract_binary = fields.Binary(
        string='Contrato generado',
    )

    def get_date_start_related_contract(self):
        if self.contract_ids:
            return self.contract_ids[0].date_start if self.contract_ids[0].date_start else False
        return False

    def get_service_duration_related_contract(self):
        if self.contract_ids:
            return self.contract_ids[0].service_duration if self.contract_ids[0].service_duration else False
        return False

    def get_render_template_contract(self):
        if self.contract_template_id:
            template_id = self.contract_template_id
            render_template = self.env['mail.template'].with_context(lang=template_id._context.get('lang'), safe=False)
            generated_field_values = render_template._render_template(
                getattr(template_id, 'body_html'), template_id.model, [self.id])
            render_template = generated_field_values[self.id]
            return render_template

    def action_generate_report_pdf(self):
        for rec in self:
            if rec.contract_template_id:
                report_name = "contract_formats.report_hr_contract"

                pdf = self.env.ref(report_name, False)._render_qweb_pdf('contract_formats.template_report_hr_contract',rec.id)[0]
                rec.contract_binary = base64.encodebytes(pdf)
                rec.contract_name = '{} - Contrato.pdf'.format(rec.name or '-')

    def action_generate_massive_report_pdf(self):
        report_name = "contract_formats.report_hr_contract"
        return self.env.ref(report_name).report_action(self)

    def create_action_leads_view(self):
        form = self.env.ref('contract_formats.mail_template_preview_view_form_inherit_contract_formats', False)
        action = {
            'name': 'Vista previa contrato',
            'type': "ir.actions.act_window",
            'view_type': "form",
            'view_mode': "form",
            'res_model': 'mail.template.preview',
            'views': [(form.id, 'form')],
            'view_id': form.id,
            'target': 'new',
            'context': {
                'template_id': self.contract_template_id.id,
                'default_res_id': self.id
            },
        }
        return action

    @api.model
    def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
        res = super(HrContract, self).fields_view_get(
            view_id=view_id, view_type=view_type, toolbar=toolbar, submenu=submenu)
        if view_type == 'form':
            contract_model = self.env.ref('hr_contract.model_hr_contract', False)
            if 'contract_template_id' in res['fields']:
                res['fields']['contract_template_id']['domain'] = [('model_id', '=', contract_model.id)]
        return res

    @api.depends('date_start', 'date_end')
    def compute_service_duration(self):
        for record in self:
            years = months = days = 0
            if record.date_start and record.date_end:
                service_until = record.date_end
                if record.date_start and service_until > record.date_start:
                    service_duration = relativedelta.relativedelta(
                        service_until,
                        record.date_start
                    )
                    years = service_duration.years
                    months = service_duration.months
                    days = service_duration.days
            service_duration = u'{} año(s) {} mes(es) {} día(s)'.format(years, months, days)
            record.service_duration = service_duration

    @api.model
    def _action_update_service_duration_on_contracts(self):
        contracts = self.search([])
        contracts.compute_service_duration()

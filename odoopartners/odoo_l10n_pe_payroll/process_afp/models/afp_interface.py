from .reports import AfpExcelReport
from odoo import fields, models, api, _
from odoo.exceptions import ValidationError
import base64


class AfpInterface(models.Model):
    _name = 'afp.interface'
    _description = 'Reporte AFP'

    company_id = fields.Many2one('res.company', 
        string='Compañía',
        required=True,
        default=lambda self: self.env.company
    )
    start_date = fields.Date(string='Fecha de Inicio'
                             )
    end_date = fields.Date(string='Fecha de Fin')
    xls_filename = fields.Char()
    xls_binary = fields.Binary('Reporte Excel')
    
    @api.depends('start_date', 'end_date')
    def _compute_display_name(self):
        for obj in self:
            if obj.start_date and obj.end_date:
                obj.display_name = '%s - %s' % (obj.start_date.strftime('%d/%m/%Y'), obj.end_date.strftime('%d/%m/%Y'))
            else:
                obj.display_name = ''

    @staticmethod
    def _get_periods(start_m, start_y, end_m, end_y):
        start = '{}/{}'.format("{:02d}".format(start_m), start_y)
        end = '{}/{}'.format("{:02d}".format(end_m), end_y)
        periods = [start]
        value = False
        if start == end:
            return periods
        while value != end:
            if start_y == end_y:
                start_m += 1
            else:
                start_m += 1
                if start_m == 13:
                    start_y += 1
                    start_m = 1
            value = '{}/{}'.format("{:02d}".format(start_m), start_y)
            periods.append(value)
        return periods

    def action_generate_report(self):
        for obj in self:
            if obj.start_date == obj.end_date:
                raise ValidationError('La fechas del periodo no pueden ser iguales.')
            if obj.start_date > obj.end_date:
                raise ValidationError('La fecha "Desde" no puede ser mayor que la fecha "Hasta".')
            
            values = []
            start_m = int(obj.start_date.strftime('%m'))
            start_y = int(obj.start_date.strftime('%Y'))
            
            # Payroll search considering the company
            company_id = obj.company_id.id or self.env.company.id
            domain = [
                ('date_from', '>=', obj.start_date),
                ('date_to', '<=', obj.end_date),
                ('employee_id.is_cuspp', '=', True),
                ('company_id', '=', company_id)
            ]
            payslip = self.env['hr.payslip'].search(domain)

            employees = payslip.mapped('employee_id')

            for employee in employees:
                employee_payslip = payslip.filtered(lambda x: x.employee_id == employee)
                rem = 0
                except_amount = ''
                work_type = 'N'
                for slip in employee_payslip:
                    line_ids = slip.line_ids.filtered(lambda x: x.code == 'BSP_001' and not x.salary_rule_id.l10n_pe_afp)
                    rem += sum(line.amount for line in line_ids)
                if rem == 0:
                    except_amount = 'L'
                begin_business_relation = 'N'
                end_business_relation = 'N'
                if employee.service_start_date and int(employee.service_start_date.strftime('%m')) == start_m and int(
                        employee.service_start_date.strftime('%Y')) == start_y:
                    begin_business_relation = 'S'
                if employee.service_termination_date and int(employee.service_termination_date.strftime('%m')) == start_m and \
                        int(employee.service_termination_date.strftime('%Y')) == start_y:
                    end_business_relation = 'S'
                if employee.pension_system_id and employee.pension_system_id.cuspp:
                    if employee.type_identification_id and employee.type_identification_id.l10n_pe_vat_code in ['1', '4', '7']:
                        if employee.type_identification_id.l10n_pe_vat_code == '1':
                            document_type_id = '0'
                        elif employee.type_identification_id.l10n_pe_vat_code == '4':
                            document_type_id = '1'
                        else:
                            document_type_id = '4'
                    else:
                        document_type_id = '5'
                    values.append({
                        'cuspp': employee.cuspp or '0',
                        'document_type_id': document_type_id,
                        'document_number': employee.identification_id or '',
                        'lastname': employee.lastname or '',
                        'secondname': employee.secondname or '',
                        'firstname': employee.firstname or '',
                        'business_relation': 'S',
                        'begin_business_relation': begin_business_relation,
                        'end_business_relation': end_business_relation,
                        'except_amount': except_amount,
                        'rem': rem,
                        'amount_vol_fin': 0,
                        'amount_vol_nfin': 0,
                        'amount_vol': 0,
                        'work_type': work_type,
                        'afp': ''
                    })
            obj.generate_excel(values)

    def generate_excel(self, data):
        report_xls = AfpExcelReport(data, self)
        values = {
            'xls_filename': report_xls.get_filename(),
            'xls_binary': base64.encodebytes(report_xls.get_content()),
        }
        self.write(values)

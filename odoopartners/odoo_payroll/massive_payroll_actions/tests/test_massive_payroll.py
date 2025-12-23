import datetime

from odoo.addons.hr_payroll.tests.common import TestPayslipBase
from dateutil.relativedelta import relativedelta


class TestPayslipFlow(TestPayslipBase):

    def test_00_payslip_flow(self):
        self.richard_emp.contract_ids[0].state = 'open'

        richard_payslip = self.env['hr.payslip'].create({
            'name': 'Payslip of Richard',
            'employee_id': self.richard_emp.id
        })

        payslip_input = self.env['hr.payslip.input'].search([('payslip_id', '=', richard_payslip.id)])
        
        payslip_input.write({'amount': 5.0})

        self.assertEqual(richard_payslip.state, 'draft', 'State not changed!')

        richard_payslip.compute_sheet()

        richard_payslip.action_payslip_done()

        self.assertEqual(richard_payslip.state, 'done', 'State not changed!')

        richard_payslip.action_payslip_paid()

        self.assertEqual(richard_payslip.state, 'paid', 'State not changed!')
        
        print(f"Estado antes del reembolso: {richard_payslip.state}")

        existing_payslip_refund = self.env['hr.payslip'].search([('name', 'like', 'Refund: '+ richard_payslip.name), ('credit_note', '=', True)])
        print(f"Refunds antes de refund_sheet: {existing_payslip_refund}")

        richard_payslip.refund_sheet()

        payslip_refund = self.env['hr.payslip'].search([('name', 'like', 'Refund: '+ richard_payslip.name), ('credit_note', '=', True)])
        print(f"Refunds después de refund_sheet: {payslip_refund}")
        
        self.assertFalse(bool(payslip_refund), "Payslip not refunded!")

        payslip_run = self.env['hr.payslip.run'].create({
            'date_end': '2011-09-30',
            'date_start': '2011-09-01',
            'name': 'Payslip for Employee'
        })

        payslip_employee = self.env['hr.payslip.employees'].create({
            'employee_ids': [(4, self.richard_emp.id)]
        })

        payslip_employee.with_context(active_id=payslip_run.id).compute_sheet()
        print('-------TEST MASSIVE PAYROLL PAYSLIP OK ----------------')


    def test_01_batch_with_specific_structure(self):
        """ Create a batch with a given structure different than the regular pay"""

        specific_structure = self.env['hr.payroll.structure'].create({
            'name': 'End of the Year Bonus - Test',
            'type_id': self.structure_type.id,
        })

        self.richard_emp.contract_ids[0].state = 'open'

        payslip_run = self.env['hr.payslip.run'].create({
            'date_start': datetime.date.today() + relativedelta(years=-1, month=8, day=1),
            'date_end': datetime.date.today() + relativedelta(years=-1, month=8, day=31),
            'name': 'End of the year bonus'
        })
        payslip_employee = self.env['hr.payslip.employees'].create({
            'employee_ids': [(4, self.richard_emp.id)],
            'structure_id': specific_structure.id,
        })

        payslip_employee.with_context(active_id=payslip_run.id).compute_sheet()

        self.assertEqual(len(payslip_run.slip_ids), 1)
        self.assertEqual(payslip_run.slip_ids.struct_id.id, specific_structure.id)
        print('-------TEST MASSIVE PAYROLL STRUCTURE OK ----------------')


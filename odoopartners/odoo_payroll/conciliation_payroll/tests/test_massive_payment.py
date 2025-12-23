from odoo.tests.common import TransactionCase


class TestMassivePayment(TransactionCase):

    def setUp(self):
        super(TestMassivePayment, self).setUp()
        self.account_account = self.env['account.account']
        self.hr_employee = self.env['hr.employee']
        self.hr_contract = self.env['hr.contract']
        self.hr_payslip = self.env['hr.payslip']
        self.hr_massive_payment = self.env['hr.massive.payment']

        # create accounts
        self.account_model = self.env['account.account']
        self.account_model_type = self.env['account.account.type'].create({
            'name': 'account',
            'type': 'other',
            'internal_group': 'equity',
        })
        self.debit_account = self.account_account.create({
            'code': 'X101',
            'name': 'Cuenta deudora',
            'user_type_id': self.account_model_type.id,
            'company_id': self.env.company.id,
        })
        self.credit_account = self.account_account.create({
            'code': 'X102',
            'name': 'Cuenta acreedora',
            'user_type_id': self.account_model_type.id,
            'company_id': self.env.company.id,
        })

        # create employee
        self.employee_1 = self.hr_employee.create({
            'name': 'Empleado 1',
        })
        self.employee_2 = self.hr_employee.create({
            'name': 'Empleado 2',
        })

        # create contracts
        self.contract_1 = self.hr_contract.create({
            'name': 'Contrato 1',
            'employee_id': self.employee_1.id,
            'wage': 1000,
            'state': 'open',
        })
        self.contract_2 = self.hr_contract.create({
            'name': 'Contrato 2',
            'employee_id': self.employee_2.id,
            'wage': 2000,
            'state': 'open',
        })

    def _create_payslip(self, employee, contract, date_from, date_to):
        return self.hr_payslip.create({
            'employee_id': employee.id,
            'contract_id': contract.id,
            'struct_id': self.env.ref('hr_payroll.structure_base').id,
            'date_from': date_from,
            'date_to': date_to,
        })

    def test_massive_payment(self):
        # payslips
        payslip_1 = self._create_payslip(self.employee_1, self.contract_1, '2023-01-01', '2023-01-31')
        payslip_2 = self._create_payslip(self.employee_2, self.contract_2, '2023-01-01', '2023-01-31')

        payslip_1.action_payslip_done()
        payslip_2.action_payslip_done()

        massive_payment = self.hr_massive_payment.create({
            'payslip_ids': [(6, 0, [payslip_1.id, payslip_2.id])],
        })

        # payment
        massive_payment.action_payslip_paid()

        # verify 'paid' state
        self.assertEqual(payslip_1.state, 'paid')
        self.assertEqual(payslip_2.state, 'paid')

        # conciliation
        massive_payment.action_reconciled()

        self.assertTrue(massive_payment.has_reconciled_entries)


#odoo@6d643bcd8d9d:/opt/odoo_dir/odoo$ ./odoo-bin -c /etc/odoo/odoo.conf -i conciliation_payroll --test-enable -p 8081 -d conciltest --stop-after-init

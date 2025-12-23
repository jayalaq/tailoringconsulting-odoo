from odoo.tests.common import tagged,TransactionCase
from datetime import *

@tagged('post_install', '-at_install')
class TestFilterUtilities(TransactionCase):
    def setUp(self):
        super().setUp()
        
        self.holiday_status = self.env['hr.leave.type'].create({
            'name': 'Ausencia de Prueba',
            'utilities': True
        })
        
        self.employee = self.env['hr.employee'].create({
            'name':'Raul Test',
        })
        self.entry_work = self.env['hr.work.entry.type'].search([('code','=','WORK100')])[0]
        self.payslip = self.env['hr.payslip'].create({
            'date_from': date(2024,8,1),
            'date_to': date(2024,8,31),
            'employee_id':self.employee.id,
            'name':self.employee.name,
            'contract_id':self.env['hr.contract'].search([])[0].id,
        })

    def test_hr_leave_utilities(self):
    
        hr_leave = self.env['hr.leave'].create({
            'holiday_status_id': self.holiday_status.id,
            'employee_id': self.employee.id, 
            'request_date_from':date.today(),
            'request_date_to':date.today() + timedelta(days=10),
            'report_attendance':True
        })
        self.assertEqual(hr_leave.holiday_status_id.id,self.holiday_status.id)
        self.assertEqual(hr_leave.employee_id.id,self.employee.id)
        self.assertEqual(hr_leave.request_date_from,date.today())
        self.assertEqual(hr_leave.request_date_to,date.today() + timedelta(days=10))

    def test_hr_attendance_utilities(self):
        hr_attendance = self.env['hr.attendance'].create({
            'employee_id': self.employee.id,
            'check_in':datetime(2024,8,5,10,00,00),
            'check_out': datetime(2024,8,5,19,00,00),
        })
        self.assertEqual(hr_attendance.employee_id.id,self.employee.id)
        self.assertEqual(hr_attendance.check_in,datetime(2024,8,5,10,00,00))
        self.assertEqual(hr_attendance.check_out,datetime(2024,8,5,19,00,00))


        
from odoo import fields
from odoo.tests import common

@common.tagged('post_install', '-at_install')
class TestHrWorkEntryType(common.TransactionCase):

    def setUp(self):
        super().setUp()
        self.work_entry_type = self.env['hr.work.entry.type'].create({
            'name':'Trabajo Home-Office',
            'code':'THO-1000',
            'is_calc_own_rule':True,
            'round_days':'NO'
        })
        self.company = self.env['res.company'].search([])
        self.task = self.env['project.task'].search([])
        self.project = self.env['project.project'].search([])
        
        self.leave_type = self.env['hr.leave.type'].create({
            'name':'Ausencia por Vacaciones',
            'code':'APV-1000',
            'leave_validation_type':'hr',
            'request_unit':'day',
            'support_document':True,
            'time_type':'leave',
            'company_id': self.company[0].id,
            'work_entry_type_id': self.work_entry_type.id,
            'timesheet_project_id': self.project[0].id,
            'timesheet_task_id': self.task[0].id  
        })
    
    def test_field_work_entry_type(self):
        self.assertEqual(self.work_entry_type.name,'Trabajo Home-Office')
        self.assertEqual(self.work_entry_type.code,'THO-1000')
        self.assertEqual(self.work_entry_type.is_calc_own_rule,True)
        self.assertEqual(self.work_entry_type.round_days,'NO')
        
        
    def test_field_hr_leave_type(self):
        self.assertEqual(self.leave_type.name,'Ausencia por Vacaciones')
        self.assertEqual(self.leave_type.code,'APV-1000')
        self.assertEqual(self.leave_type.leave_validation_type,'hr')
        self.assertEqual(self.leave_type.request_unit,'day')
        self.assertEqual(self.leave_type.support_document,True)
        self.assertEqual(self.leave_type.time_type,'leave')
        self.assertEqual(self.leave_type.company_id.id,self.company[0].id)
        self.assertEqual(self.leave_type.work_entry_type_id.id,self.work_entry_type.id)
        self.assertEqual(self.leave_type.timesheet_project_id.id,self.project[0].id)
        self.assertEqual(self.leave_type.timesheet_task_id.id, self.task[0].id)
        
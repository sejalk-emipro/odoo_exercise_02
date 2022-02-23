# -*- coding :utf-8 -*-

from openerp import models,fields

class Employee(models.Model):

    _name="employee.ept"
    _description="Employee"

    name=fields.Char(string="Employee Name",help="Name of the employee",required=True)
    position=fields.Char(string="Job Position",help="Job position of the employee")
    salary=fields.Float(string="Salary",help="Salary of the employee",digits=(6,2))
    hire_date=fields.Date(string="Hire Date",help="Enter hire date of the employee")
    gender=fields.Selection([('Male','Male'),('Female','Female'),('Transgender','Transgender')],string="Gender")
    job_type=fields.Selection([('Permanent','Permanent'),('Adhoc','Adhoc')])
    is_manager=fields.Boolean(string="Is Manager")
    manager_id= fields.Many2one(comodel_name="employee.ept",string='Manager')
    user_id=fields.Many2one(comodel_name="res.users",string='Related User')
    department_id = fields.Many2one(comodel_name="employee.department.ept", string='Department',required=True)
    shift_id=fields.Many2one(comodel_name="employee.department.shift.ept", string='Shift',required=True)
    employee_ids=fields.One2many(comodel_name="employee.ept",inverse_name="manager_id",string='Manager',readonly=True)
    increment_percentage=fields.Float(string="Increment Percentage",help="Increment percentage of the employee")

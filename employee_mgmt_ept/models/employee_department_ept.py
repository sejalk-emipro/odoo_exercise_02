# -*- coding :utf-8 -*-

from openerp import models,fields

class Department(models.Model):

    _name="employee.department.ept"
    _description="Employee Department"

    name=fields.Char(string="Name",help="Name of the Department",required=True)
    employee_ids=fields.One2many(comodel_name="employee.ept",inverse_name="department_id",string="Employee",help="List of employee")
    depart_manager_id=fields.Many2one(comodel_name="res.users",string="Department Manager")


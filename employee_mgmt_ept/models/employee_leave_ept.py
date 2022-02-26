# -*- coding :utf-8 -*-

from openerp import models,fields

class Leave(models.Model):

    _name="employee.leave.ept"
    _description="Employee Leave"

    employee_id = fields.Many2one(comodel_name="employee.ept", string='Employee')
    department_id = fields.Many2one(comodel_name="employee.department.ept", string='Department',
                                    related='employee_id.department_id',
                                    store=False, readonly=True)
    start_date=fields.Date(String="Start Date",help="Start date of the leave",copy=False)
    end_date=fields.Date(String="End Date",help="End date of the leave",copy=False)
    status=fields.Selection([('Draft','Draft'),('Approved','Approved')
                             ,('Refused','Refused'),('Cancelled','Cancelled')],default='Draft',string="Status",help="Status of the leave")
    description=fields.Char(string="Description",help="Description of the leave",required=True,copy=False)
# -*- coding :utf-8 -*-

from openerp import models, fields


class EmployeeComments(models.Model):

    _name = "employee.comments"
    _description = "Employee Comments"
    _rec_name = "comment"
    _order = "id desc"

    comment = fields.Text(string="Employee Comments", help="Employee comments against the remarks or improvement.")
    date = fields.Date(string="Comment Date", default=fields.Date.today(),
                       help="Comment date")
    employee_remarks_id = fields.Many2one(comodel_name="employee.remarks", string="Remarks",
                                          help="Employee Remarks Ref.")




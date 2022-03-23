# -*- coding :utf-8 -*-

from openerp import models, fields,api


class EmployeeComment(models.TransientModel):

    _name = "employee.comment"
    _description = "Employee Comment"

    comment = fields.Text(string="Employee Comments",required=True, help="Employee comments against the remarks or improvement.")
    date = fields.Date(string="Date", default=fields.Date.today(),help="Replied date")
    employee_remarks_id = fields.Many2one(comodel_name="employee.remarks", string="Remarks",
                                          help="Employee Remarks Ref.")

    @api.multi
    def reply(self):
        """
        :functionality : replied by the employee against the improvement remarks
        :return: -
        """
        active_ids=self.env.context.get('active_ids')

        employee_remark = self.env['employee.remarks'].browse(active_ids[0])

        comments=[(0,0,{'comment':self.comment,'employee_remarks_id':employee_remark.id})]

        employee_remark.write({'state':'Replied by employee',
                               'employee_comment_ids':comments})


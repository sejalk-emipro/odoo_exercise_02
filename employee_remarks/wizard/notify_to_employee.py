# -*- coding :utf-8 -*-

from datetime import datetime
from dateutil.relativedelta import relativedelta
from openerp import models, fields,api



class NotifyToEmployee(models.TransientModel):

    _name = "notify.employee"
    _description = "Notify To Employee"

    review = fields.Selection([('Positive', 'Positive'), ('Negative', 'Negative')],
                              string="Review", help="Select the review of the employee remarks")
    date = fields.Date(string="Creation Date", default=fields.Date.today(),
                       help="Creation date of the improvement remark")
    improvement_days = fields.Integer(string="Improvement Days",
                                      help="Enter the improvement days of the employee remarks")
    next_date = fields.Date(string="Remainder Date", help="Auto calculate reminder date")
    employee_remarks_id = fields.Many2one(comodel_name="employee.remarks", string="Remarks",
                                          help="Employee Remarks Ref.")

    @api.onchange('improvement_days')
    def onchange_Improvement_days(self):
        if self.improvement_days>0:
            self.next_date= datetime.today() + relativedelta(days=self.improvement_days)

    @api.multi
    def notifytoemployee(self):
        active_ids=self.env.context.get('active_ids')
        employee_remark=self.env['employee.remarks'].browse(active_ids[0])

        improvement_remarks=[(0,0,{
            'review':employee_remark.review,
            'remark':employee_remark.remark,
            'improvement_days':self.improvement_days,
            'next_date':datetime.today() + relativedelta(days=self.improvement_days)
        })]

        employee_remark.write({'state':'Notify to Employee','display_remark_to_employee':True,
                               'improvement_remark_ids':improvement_remarks})

        template_id = self.env.ref('employee_remarks.email_template_send_notification_to_employee')
        if template_id:
            template_id.send_mail(employee_remark.id, True)

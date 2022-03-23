# -*- coding :utf-8 -*-

from datetime import datetime
from dateutil.relativedelta import relativedelta
from openerp import models, fields,api

class ImprovementRemark(models.TransientModel):

    _name = "improvement.remark"
    _description = "Improvement Remarks"

    review = fields.Selection([('Positive', 'Positive'), ('Negative', 'Negative')],
                              string="Review", help="Select the review of the employee remarks",required=True)
    remark = fields.Text(string="Improvement Remark",required=True, help="Enter improvement remarks of the selected employee.")
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
    def create_improvement_remark(self):
        active_ids=self.env.context.get('active_ids')
        employee_remark=self.env['employee.remarks'].browse(active_ids[0])
        improvement_remarks=[(0,0,{
            'review':self.review,
            'remark':self.remark,
            'improvement_days':self.improvement_days,
            'next_date':datetime.today() + relativedelta(days=self.improvement_days)
        })]
        employee_remark.write({'review':self.review,
            'state':'Notify to Employee',
            'improvement_remark_ids':improvement_remarks})

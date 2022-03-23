# -*- coding :utf-8 -*-

from openerp import models, fields


class ImprovementRemarks(models.Model):

    _name = "improvement.remarks"
    _description = "Improvement Remarks"
    _rec_name = "remark"
    _order = "id desc"

    review = fields.Selection([('Positive', 'Positive'), ('Negative', 'Negative')],
                              string="Review", help="Select the review of the employee remarks")
    remark = fields.Text(string="Improvement Remark", help="Enter improvement remarks of the selected employee.")
    date = fields.Date(string="Creation Date", default=fields.Date.today(),
                       help="Creation date of the improvement remark")
    improvement_days = fields.Integer(string="Improvement Days",
                                      help="Enter the improvement days of the employee remarks")
    next_date = fields.Date(string="Remainder Date", help="Auto calculate reminder date")
    employee_remarks_id = fields.Many2one(comodel_name="employee.remarks", string="Remarks",
                                          help="Employee Remarks Ref.")



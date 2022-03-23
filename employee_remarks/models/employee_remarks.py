# -*- coding :utf-8 -*-

from openerp import models, fields,api


class EmployeeRemarks(models.Model):

    _name = "employee.remarks"
    _description = "Employee Remarks"
    _rec_name = "sequence"
    _order = "id desc"

    sequence=fields.Char(string="Sequence",help="Sequence of the employee remarks.")
    employee_id=fields.Many2one(comodel_name="hr.employee",string="Employee",help="Select employee for the remarks")
    remark_type_id=fields.Many2one(comodel_name="remark.type",
                                   string="Remark Type",help="Select remark type for the employee remark.")
    remark=fields.Text(string="Remark",help="Enter remarks of the selected employee.")
    review=fields.Selection([('Positive','Positive'),('Negative','Negative')],
                            string="Review",help="Select the review of the employee remarks")
    state=fields.Selection([('New','New'),('Notify to Employee','Notify to Employee'),('Replied by employee','Replied by employee')]
                           ,string="State",help="State of the employee remarks",default="New")
    date=fields.Date(string="Creation Date",default=fields.Date.today(),help="Creation date of the employee remark")
    display_remark_to_employee=fields.Boolean(string="Display Remark to Employee",
                                              help="This flag use to display remark of the employee")
    reviewer_id=fields.Many2one(comodel_name="res.users",string="Reviewer",help="Select name of the reviewer")
    improvement_remark_ids=fields.One2many(comodel_name="improvement.remarks",inverse_name="employee_remarks_id",string="Improvement Remarks",help="Improvement remarks ref")
    employee_comment_ids = fields.One2many(comodel_name="employee.comments", inverse_name="employee_remarks_id",
                                             string="Employee Comments", help="Employee Comments")
    isremarks=fields.Boolean(string="Remarks",compute="compute_isremark",store=False,search="fnct_search_no_of_notify")


    def fnct_search_no_of_notify(self,operator, value):
        """
            :functionality : filter the more than five negative remarks of employees
            :param operator: Operator for domain.
            :param value: Value for domain.
            :returns: list (domain)
        """
        self._cr.execute("""            
            SELECT ar.id FROM employee_remarks AS ar 
            JOIN improvement_remarks ir ON ir.employee_remarks_id= ar.id AND ir.review = 'Negative'
            GROUP BY ar.id
            HAVING COUNT(ir.id) >=5
        """)

        remark_ids = map(lambda remark_id: remark_id and remark_id[0], set(self._cr.fetchall()))
        return [('id', 'in', remark_ids)]

    def compute_isremark(self):
        for notes in self:
            notes.isremarks = False
            negative_count=len(notes.improvement_remark_ids.filtered(lambda remark:remark.review=="Negative"))
            if negative_count>=5:
                notes.isremarks=True

    @api.model
    def create(self, vals):
        vals['sequence'] = self.env['ir.sequence'].next_by_code('employee.remark') or 'New'
        remarks = super(EmployeeRemarks, self).create(vals)
        return remarks









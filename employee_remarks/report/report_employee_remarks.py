# -*- coding: utf-8 -*-

from openerp import models,fields
from openerp.tools.sql import drop_view_if_exists

class ReportEmployeeRemark(models.AbstractModel):

    _name="report.employee_remarks.remark"
    _description="Employee Remarks"
    _auto = False

    sequence = fields.Char(string="Sequence", readonly=True)
    employee_id = fields.Many2one(comodel_name="hr.employee", string="Employee", readonly=True)
    remark_type_id = fields.Many2one(comodel_name="remark.type",
                                     string="Remark Type", readonly=True)
    remark = fields.Text(string="Remark", readonly=True)
    review = fields.Selection([('Positive', 'Positive'), ('Negative', 'Negative')],
                              string="Review", readonly=True)
    state = fields.Selection(
        [('New', 'New'), ('Notify to Employee', 'Notify to Employee'), ('Replied by employee', 'Replied by employee')]
        , string="State",readonly=True,)
    date = fields.Date(string="Creation Date", default=fields.Date.today(), readonly=True)
    reviewer_id = fields.Many2one(comodel_name="res.users", string="Reviewer", readonly=True)


    def init(self, cr):
        drop_view_if_exists(cr, 'report_employee_remarks_remark')
        cr.execute("""
            create or replace view report_employee_remarks_remark as (
               select er.sequence,er.employee_id ,er.remark_type_id,er.review,er.remark,er.state,er.date,er.reviewer_id
               from employee_remarks er
               order by er.sequence desc
            )""")
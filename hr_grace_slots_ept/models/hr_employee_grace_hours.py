# -*- coding :utf-8 -*-

from openerp import models,fields,api
from datetime import datetime, date
from dateutil.relativedelta import relativedelta

class HREmployeeGraceHours(models.Model):

    _name="hr.employee.grace.hours"
    _description="Employee Grace hours"

    name=fields.Char(string="Name",required=True,help="Name of the employee grace hour slots")
    employee_id=fields.Many2one(comodel_name="hr.employee",string="Employee")
    grace_hour_id=fields.Many2one(comodel_name="hr.grace.hour",string="Grace Slot",required=True)
    date_from = fields.Date(string="Date From", help="From date of the  Employee Grace Hours Slots", required=1)
    date_to = fields.Date(string="Date To", required=1,help="End date of the  Employee Grace Hours Slots")
    consumed_time_minutes=fields.Integer(string = "Consumed time",store=False ,compute="calculate_consumed_time")

    def calculate_consumed_time(self):
        time=0

    @api.multi
    def employee_grace_hours_slot_allocation(self):
        """
        :functionality :
        :return: -
        """
        # employee_ids=self.pool.get('hr.employee').search([('job_id.hr_grace_hour_id','!=',False)])

        employee_ids=self.env['hr.employee'].search([('job_id.hr_grace_hour_id','!=',False)])
        date=fields.Date.today()
        from_date_of_month = datetime.strftime(datetime(datetime.now().year, datetime.now().month, 1).date(), '%Y-%m-%d')
        to_date_of_month=datetime.strftime((datetime(datetime.now().year,datetime.now().month,1) + relativedelta(months=1, days=-1)).date(), '%Y-%m-%d')

        for employee in employee_ids:
            if employee.job_id:
                 self.env['hr.employee.grace.hours'].create({
                    'name':employee.job_id.hr_grace_hour_id.name,
                    'employee_id':employee.id,
                    'grace_hour_id':employee.job_id.hr_grace_hour_id.id,
                    'date_from':from_date_of_month,
                    'date_to':to_date_of_month,
                    'consumed_time_minutes':0
                })




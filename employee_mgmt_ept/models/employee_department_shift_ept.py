#-*- coding :utf-8 -*-

from openerp import models,fields

class Shift(models.Model):

    _name="employee.department.shift.ept"
    _description="Shift"

    name=fields.Selection([('Morning','Morning'),('Afternoon','Afternoon'),('Evening','Evening'),('Night','Night')], string="Shift")
    employee_ids=fields.One2many(comodel_name="employee.ept",inverse_name="shift_id",string="Employee")

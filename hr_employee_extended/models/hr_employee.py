from openerp import models,fields

class HREmployee(models.Model):

    _name="hr.employee"
    _inherit="hr.employee"

    employee_credentials_ids=fields.One2many(comodel_name="hr.employee.credentials",inverse_name="employee_id",string="Employee Credentials")
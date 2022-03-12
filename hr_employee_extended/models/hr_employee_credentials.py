from openerp import models,fields

class HREmployeeCredentials(models.Model):

    _name="hr.employee.credentials"
    _description="Employee Credentials"

    name=fields.Char(string="Username",required=True,help="Username of the employee")
    password=fields.Char(string="Password",help="Password")
    login_for=fields.Char(string="Login",required=True)
    employee_id=fields.Many2one(comodel_name="hr.employee",string="Employee",help="Hr Employee Ref")

# -*- coding :utf-8 -*-

from openerp import models,fields

class AccountTaxEpt(models.Model):

    _name="account.tax.ept"
    _description="Account Tax"

    name=fields.Char(string="Name",help="Name of the account tax")
    tax_use=fields.Selection([('None','None'),('Sales','Sales'),('Purchase','Purchase')],string="Tax Use",default="None")
    tax_value=fields.Float(string="Amount",digits=(16,2),help="Tax value",default=0.0)
    tax_amount_type=fields.Selection([('Percentage','Percentage'),('Fixed','Fixed')],string="Tax Amount Type",default="Percentage")


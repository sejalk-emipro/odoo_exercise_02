
from openerp import models,fields

class SaleOrder(models.Model):

    _name="sale.order"
    _inherit="sale.order"

    opportunity_id=fields.Many2one(comodel_name="crm.lead",string="CRM Lead Opportunity",help="CRM Lead")

# -*- coding :utf-8 -*-

from openerp import models,fields

class SaleOrderEPT(models.Model):
    _name="sale.order.ept"
    _description="Sale Order"

    name=fields.Char(string="Order No",help="Number of the order",required=True)
    partner_id=fields.Many2one(comodel_name="res.partner.ept",string="Customer",required=True,
                                domain=[('parent_id','=',False)])
    partner_invoice_id=fields.Many2one(comodel_name="res.partner.ept",string="Invoice Customer",required=True,
                                       domain="[('address_type','=','Invoice'),('parent_id','=',partner_id)]")
    partner_shipping_id=fields.Many2one(comodel_name="res.partner.ept",string="Shipping Customer",required=True,
                                       domain="[('address_type','=','Shipping'),('parent_id','=',partner_id)]")
    sale_order_date=fields.Date(string="Sale Order Date",help="Date of the sale order",default=fields.Date.today())
    sale_person_id=fields.Many2one(comodel_name="res.users",string="Sales Person")
    state=fields.Selection([('Draft','Draft'),('Confirmed','Confirmed'),('Done','Done'),('Cancelled','Cancelled')],string="State",help="State of the order",default="Draft")

    order_line_ids=fields.One2many(comodel_name="sale.order.line.ept",inverse_name="order_id",string="Order line")





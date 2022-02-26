# -*- coding :utf-8 -*-

from openerp import models,fields

class SaleOrderLine(models.Model):

    _name="sale.order.line.ept"
    _description="Sale Order Line"

    order_id=fields.Many2one(comodel_name="sale.order.ept",string="Sale order")
    product_id=fields.Many2one(comodel_name="product.ept",string="product")
    description=fields.Text(string="Description",help="description of the product")
    quantity=fields.Float(string="Quantity",digits=(16,2),help="Quantity of the product of sale order")
    unit_price=fields.Float(string="Unit price",digits=(16,2),help="Unit price of the product")
    state=fields.Selection([('Draft','Draft'),('Confirmed','Confirmed'),('Cancelled','Cancelled')],string="State",help="State of the order line",default="Draft")
    uom_id=fields.Many2one(comodel_name="product.uom.ept",string="UoM")
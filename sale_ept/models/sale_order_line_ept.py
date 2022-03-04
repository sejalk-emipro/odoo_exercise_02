# -*- coding :utf-8 -*-

from openerp import models,fields,api

class SaleOrderLine(models.Model):

    _name="sale.order.line.ept"
    _description="Sale Order Line"

    order_id=fields.Many2one(comodel_name="sale.order.ept",string="Sale order")
    product_id=fields.Many2one(comodel_name="product.ept",string="product")
    name=fields.Text(string="Description",help="description of the product")
    quantity=fields.Float(string="Quantity",digits=(16,2),help="Quantity of the product of sale order")
    unit_price=fields.Float(string="Unit price",digits=(16,2),help="Unit price of the product")
    state=fields.Selection([('Draft','Draft'),('Confirmed','Confirmed'),('Cancelled','Cancelled')],string="State",help="State of the order line",default="Draft")
    uom_id=fields.Many2one(comodel_name="product.uom.ept",string="UoM")
    subtotal=fields.Float(string="Subtotal",compute="Compute_subtotal_nostore",store=False)
    subtotal_without_tax = fields.Float(string="Subtotal Without Tax", compute="Compute_subtotal", store=True)


    @api.depends('quantity','unit_price')
    def Compute_subtotal(self):
        for order_line in self:
            order_line.subtotal_without_tax=order_line.quantity * order_line.unit_price

    def Compute_subtotal_nostore(self):
        for line in self:
            line.sub_total=line.quantity * line.unit_price



    @api.onchange('product_id')
    def onchange_product_id(self):
        if self.product_id:
            self.unit_price=self.product_id.sale_price
            self.quantity=1
            self.name = self.product_id.description
            if not self.name:
                self.name = self.product_id.name
            self.uom_id = self.product_id.uom_id.id



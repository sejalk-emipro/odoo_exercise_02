# -*- coding :utf-8  -*-

from openerp import models,fields,api

class PurchaseOrderLineEpt(models.Model):
    _name="purchase.order.line.ept"
    _description="Purchase Order Line"

    purchase_order_id=fields.Many2one(comodel_name="purchase.order.ept",string="Purchase order")
    product_id = fields.Many2one(comodel_name="product.ept", string="product")
    name = fields.Text(string="Description", help="description of the product")
    quantity = fields.Float(string="Quantity", digits=(16, 2), help="Quantity of the product of purchase order")
    cost_price = fields.Float(string="Cost price", digits=(16, 2), help="Unit price of the product")
    state = fields.Selection([('Draft', 'Draft'), ('Confirmed', 'Confirmed'), ('Cancelled', 'Cancelled')],
                             string="State", help="State of the order line", default="Draft")
    uom_id = fields.Many2one(comodel_name="product.uom.ept", string="UoM")

    @api.onchange('product_id')
    def onchange_product_id(self):
        if self.product_id:
            self.name = self.product_id.description
            if not self.name:
                self.name = self.product_id.name
            self.uom_id = self.product_id.uom_id.id
            self.cost_price=self.product_id.cost_price


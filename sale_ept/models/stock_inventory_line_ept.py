# -*- coding :utf-8 -*-

from openerp import models,fields,api

class StockInventoryLineEpt(models.Model):

    _name="stock.inventory.line.ept"
    _description="Stock Inventory Line"

    product_id = fields.Many2one(comodel_name="product.ept", string="products",required=True)
    available_qty=fields.Float(string="System Quantity",readonly=True,help="quantity of the product")
    counted_product_qty =fields.Float(string="Counted Quantity",help="Counted Quantity")
    difference=fields.Float(string="Difference",help="difference of product quantity",
                            store=False,compute="compute_difference",readonly=True)
    inventory_id=fields.Many2one(comodel_name="stock.inventory.ept",string="Stock Inventory")

    @api.depends('inventory_id.inventory_line_ids.counted_product_qty')
    def compute_difference(self):
        for line in self:
            line.difference=(line.counted_product_qty-line.available_qty)
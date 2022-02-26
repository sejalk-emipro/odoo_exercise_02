# -*- coding :utf-8 -*-

from openerp import models,fields

class ProductData(models.Model):

    _name="product.ept"
    _description="Product"

    name = fields.Char(string="Name",required=True,help="Name of the product.")
    sku = fields.Char(string="SKU",required=True,help="SKU of the product")
    weight = fields.Float(string="Weight",digits=(16,2),help="Weight of the product")
    length = fields.Float(string="Length",digits=(16,2),help="Length of the product")
    volume = fields.Float(string="volume", digits=(16,2), help="volume of the product")
    width = fields.Float(string="width", digits=(16,2), help="width of the product")
    barcode = fields.Char(string="Barcode",help="Barcode of the product")
    product_type = fields.Selection([('Storable','Storable'),('Consumable','Consumable'),('Service','Service')],string="Product Type")
    sale_price = fields.Float(string="Sale Price", digits=(16,2), help="sale price of the product",default=1.00)
    cost_price = fields.Float(string="Cost Price", digits=(16,2), help="Cost price of the product",default=1.00)
    description = fields.Text(string="Description",help="Description of the product")
    category_id = fields.Many2one(string="Category", comodel_name="product.category.ept")
    uom_id = fields.Many2one(string="UoM",comodel_name="product.uom.ept")
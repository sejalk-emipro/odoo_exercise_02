# -*- coding :utf-8 -*-

from openerp import models,fields

class Product_UOM_Category(models.Model):

    _name="product.uom.category.ept"
    _description="Product uom Category"

    name=fields.Char(string="Name",help="Name of the actual unit of measurement of the product category")
    uom_ids=fields.One2many(string="Product UoM",comodel_name="product.uom.ept",inverse_name="uom_category_id")

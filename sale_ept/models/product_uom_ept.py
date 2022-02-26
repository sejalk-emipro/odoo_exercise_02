# -*- coding :utf-8 -*-

from openerp import models,fields

class Product_UoM(models.Model):

    _name="product.uom.ept"
    _description="Product UoM"

    name=fields.Char(string="Name",help="Name of the actual unit of measurement of product")
    uom_category_id=fields.Many2one(comodel_name="product.uom.category.ept",string="Product UoM Category")


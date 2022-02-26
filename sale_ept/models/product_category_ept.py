# -*- coding :utf-8 -*-

from openerp import models,fields

class ProductCategoty(models.Model):

    _name="product.category.ept"
    _description="Product Category"

    name=fields.Char(string="Product Category",help="Category of the product.",required=True)
    parent_id=fields.Many2one(string="Parent",comodel_name="product.category.ept")


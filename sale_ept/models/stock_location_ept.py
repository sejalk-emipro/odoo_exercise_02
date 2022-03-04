#-*- coding :utf-8 -*-

from openerp import models,fields

class StockLocationEpt(models.Model):
    _name="stock.location.ept"
    _description="Stock Location"

    name=fields.Char(string="Name",help="Name of the location",required=True)
    parent_id=fields.Many2one(comodel_name="stock.location.ept",string="Parent",help="Parent of the location's")
    location_type=fields.Selection([('Vendor','Vendor'),('Customer','Customer'), ('Internal','Internal'),
                                    ('Inventory Loss','Inventory Loss'),('Production','Production'),
                                    ('Transit','Transit'),('View','View')],string="Location Type",help="Types of the location, selected location type")
    is_scrap_location=fields.Boolean(string="Is Scrap Location",help="Flag for the Scrap location")

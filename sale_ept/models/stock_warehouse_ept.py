# -*- coding :utf-8 -*-

from openerp import models,fields,api

class StockWarehouseEpt(models.Model):
    _name="stock.warehouse.ept"
    _description="Stock Warehouse"

    name=fields.Char(string="Name",help="Name of the warehouse",required=True)
    short_code=fields.Char(string="Short Code",help="Short code of the warehouse",required=True)
    address_id=fields.Many2one(comodel_name="res.partner.ept",string="Address")
    stock_location_id=fields.Many2one(comodel_name="stock.location.ept",string="Stock Location",
                                      domain="[('location_type','=','Internal')]")
    view_location_id=fields.Many2one(comodel_name="stock.location.ept",string="View Location",
                                     domain="[('location_type','=','View')]")

    @api.model
    def create(self,vals):
        tmp_view_location=self.env['stock.location.ept'].create({
            'name':'View Location',
            'location_type':'View',
        })

        tmp_stock_location=self.env['stock.location.ept'].create({
            'name':'Stock Location',
            'location_type':'Internal',
            'parent_id':tmp_view_location.id
        })
        
        vals.update({'stock_location_id':tmp_stock_location.id,'view_location_id':tmp_view_location.id})
        return super(StockWarehouseEpt, self).create(vals)
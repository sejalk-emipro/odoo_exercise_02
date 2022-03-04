# -*- coding :utf-8 -*-

from openerp import models,fields

class StockMoveEpt(models.Model):
    _name="stock.move.ept"
    _description="Stock Move"

    name=fields.Char(string="Description",help="Description of the stock move")
    product_id = fields.Many2one(comodel_name="product.ept", string="products",required=True,help="products of the order")
    uom_id = fields.Many2one(comodel_name="product.uom.ept", string="UoM",required=True)
    source_location_id=fields.Many2one(comodel_name="stock.location.ept",string="Source Location")
    destination_location_id=fields.Many2one(comodel_name="stock.location.ept",string="Destination Location")
    qty_to_deliver=fields.Float(string="Demand",readonly=True,help="Demanded quantity of the product")
    qty_done=fields.Float(string="Done Quantities",help="Done Quantities")
    state = fields.Selection([('Draft', 'Draft'), ('Done', 'Done'), ('Cancelled', 'Cancelled')], string="State",
                             default="Draft")
    sale_line_id =fields.Many2one(comodel_name="sale.order.line.ept",string="Sale Order Lines")
    purchase_line_id=fields.Many2one(comodel_name="purchase.order.line.ept",string="Purchase Order Line Item")
    picking_id=fields.Many2one(comodel_name="stock.picking.ept",string="Picking")
    stock_inventory_id=fields.Many2one(comodel_name="stock.inventory.ept",string="Inventory")


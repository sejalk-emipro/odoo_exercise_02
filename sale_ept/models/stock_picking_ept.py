# -*- coding :utf-8 -*-

from openerp import models,fields,api

class StockPickingEpt(models.Model):
    _name="stock.picking.ept"
    _description="Stock Picking"

    name=fields.Char(string="Name",help="Name of the stock picking")
    partner_id=fields.Many2one(comodel_name="res.partner.ept",string="Partner",help="Partner of the stock picking")
    state=fields.Selection([('Draft','Draft'),('Done','Done'),('Cancelled','Cancelled')],string="State",default="Draft")
    sale_order_id =fields.Many2one(comodel_name="sale.order.ept",string="Sale Order",help="Sales order")
    purchase_order_id=fields.Many2one(comodel_name="purchase.order.ept",string="Purchase Order",help="Purchase order")
    transaction_type =fields.Selection([('In','In'),('Out','Out')],string="Transaction Type",help="Select the transaction type")
    move_ids=fields.One2many(comodel_name="stock.move.ept",inverse_name="picking_id",string="Stock Moves",help="Moves of stock picking")
    transaction_date=fields.Date(string="Transaction Date",default=fields.Date.today(),help="Transaction Date of stock picking")
    
    
    @api.model
    def create(self,vals):
        if ('name' not in vals) or (vals.get('name') in ('/', False)):
            if vals.get('sale_order_id'):
                vals['name']=self.env['ir.sequence'].next_by_code('my.stock.picking.Out') or 'New'
            if vals.get('purchase_order_id'):
                vals['name'] = self.env['ir.sequence'].next_by_code('my.stock.picking.in') or 'New'
        return super(StockPickingEpt, self).create(vals)

    @api.multi
    def validate_stock_picking(self):
        for move in self.move_ids:
            move.write({'state':'Done'})
        self.write({'state':'Done'})

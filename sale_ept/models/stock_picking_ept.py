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
    back_order_id=fields.Many2one(comodel_name="stock.picking.ept",string="Back Order")
    
    @api.model
    def create(self,vals):
        if ('name' not in vals) or (vals.get('name') in ('/', False)):
            if vals.get('transaction_type')=='Out':
                vals['name']=self.env['ir.sequence'].next_by_code('my.stock.picking.Out') or 'New'
            if vals.get('transaction_type')=='In':
                vals['name'] = self.env['ir.sequence'].next_by_code('my.stock.picking.in') or 'New'
        return super(StockPickingEpt, self).create(vals)

    @api.multi
    def cancel_stock_picking(self):
        for move in self.move_ids:
            move.write({'state':'Cancelled','qty_done':move.qty_to_deliver})
        self.write({'state':'Cancelled'})

    @api.multi
    def validate_stock_picking(self):
        """
        :functionality : validate the stock picking and create the moves
        :return: -
        """
        sum_done_qty=sum(self.move_ids.mapped('qty_done'))
        if sum_done_qty==0:
            raise Warning("done quantity not there in order")

        tmp_stock_moves=[]
        for move in self.move_ids:
            if move.qty_to_deliver<move.qty_done:
                raise Warning("Enter the valid done quantity")

            if move.qty_to_deliver!=move.qty_done:
                tmp_qty_to_deliver=move.qty_to_deliver-move.qty_done

                fields_name='sale_line_id' if self.transaction_type == 'Out' else 'purchase_line_id'
                order_line_id=move.sale_line_id if self.transaction_type == 'Out' else move.purchase_line_id

                tmp_stock_moves.append((0,0,{fields_name:order_line_id.id,
                'name':move.name,'product_id':move.product_id.id,
                'uom_id':move.uom_id.id,
                'source_location_id':move.source_location_id.id,
                'destination_location_id':move.destination_location_id.id,
                'qty_to_deliver':tmp_qty_to_deliver,'qty_done':0.0
                }))

                move.write({'state': 'Done', 'qty_to_deliver': move.qty_done})

                if move.qty_done==0:
                    move.unlink()
            else:
                move.write({'state':'Done','qty_done':move.qty_to_deliver})

        if tmp_stock_moves:
            fields_name = 'sale_order_id' if self.transaction_type == 'Out' else 'purchase_order_id'
            order_id = self.sale_order_id if self.transaction_type == 'Out' else move.purchase_line_id

            tmp_stock_picking = self.env['stock.picking.ept'].create({
                'partner_id': self.partner_id.id,
                 fields_name: order_id.id,
                'transaction_type': self.transaction_type,
                'back_order_id':self.id,
                'move_ids': tmp_stock_moves})

        self.write({'state':'Done'})

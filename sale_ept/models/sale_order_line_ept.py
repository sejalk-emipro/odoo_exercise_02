# -*- coding :utf-8 -*-

from openerp import models,fields,api
import functools

class SaleOrderLine(models.Model):

    _name="sale.order.line.ept"
    _description="Sale Order Line"

    order_id=fields.Many2one(comodel_name="sale.order.ept",string="Sale order")
    product_id=fields.Many2one(comodel_name="product.ept",string="product")
    name=fields.Text(string="Description",help="description of the product")
    quantity=fields.Float(string="Quantity",digits=(16,2),help="Quantity of the product of sale order")
    unit_price=fields.Float(string="Unit price",digits=(16,2),help="Unit price of the product")
    state=fields.Selection([('Draft','Draft'),('Confirmed','Confirmed'),('Cancelled','Cancelled')],string="State",help="State of the order line",default="Draft")
    uom_id=fields.Many2one(comodel_name="product.uom.ept",string="UoM")
    subtotal=fields.Float(string="Subtotal",compute="Compute_subtotal_nostore",store=False)
    subtotal_without_tax = fields.Float(string="Subtotal Without Tax", compute="Compute_subtotal", store=True)
    stock_move_ids = fields.One2many(comodel_name="stock.move.ept", inverse_name="sale_line_id",
                                     string="Stock Moves",readonly=True)
    delivered_qty = fields.Float(string="Delivered Quantity",store=False,compute="compute_delivered_qty",help="Total of delivered quantity")
    cancelled_qty  = fields.Float(string="Cancelled Quantity", store=False, compute="compute_cancelled_qty",
                                 help="Total of cancelled quantity")
    warehouse_id=fields.Many2one(comodel_name="stock.warehouse.ept",string="Warehouse")
    tax_ids=fields.Many2many(comodel_name="account.tax.ept",string="Tax")
    subtotal_with_tax=fields.Float(string="Subtotal With Tax",store=True,compute="compute_subtotal_tax",digits=(16,2))

    @api.depends('quantity', 'unit_price','product_id','tax_ids')
    def compute_subtotal_tax(self):
        tax_amount=0.0
        for line in self:
            for tax in line.tax_ids:
                if tax.tax_amount_type=='Percentage':
                    tax_amount+=(line.subtotal_without_tax * tax.tax_value)/100
                else:
                    tax_amount+=tax.tax_value
            self.subtotal_with_tax=(line.subtotal_without_tax+tax_amount)


    def compute_delivered_qty(self):
        for line in self:
            total_delivered_qty = 0

            total_delivered_qty=sum(line.stock_move_ids.filtered(lambda move: move.state == 'Done' and move.qty_done != 0).mapped('qty_done'))

            # for move in line.stock_move_ids:
            #     if move.state == 'Done' and move.qty_done != 0:
            #         total_delivered_qty += move.qty_to_deliver
            line.delivered_qty = total_delivered_qty

    def compute_cancelled_qty(self):
        for line in self:
            total_cancelled_qty = 0

            total_delivered_qty = sum(line.stock_move_ids.filtered(lambda move: move.state == 'Cancelled').mapped(
                    'qty_done'))

            line.cancelled_qty = total_cancelled_qty

    @api.depends('quantity','unit_price')
    def Compute_subtotal(self):
        for order_line in self:
            order_line.subtotal_without_tax=order_line.quantity * order_line.unit_price

    def Compute_subtotal_nostore(self):
        for line in self:
            line.sub_total=line.quantity * line.unit_price

    @api.onchange('product_id')
    def onchange_product_id(self):
        if self.product_id:
            self.unit_price=self.product_id.sale_price
            self.quantity=1
            self.name = self.product_id.description
            if not self.name:
                self.name = self.product_id.name
            self.uom_id = self.product_id.uom_id.id
            self.tax_ids=self.product_id.tax_ids



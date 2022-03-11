# -*- coding :utf-8  -*-

from openerp import models,fields,api

class PurchaseOrderEpt(models.Model):
    _name="purchase.order.ept"
    _description="Purchase Order"

    name=fields.Char(string="Order No",help="Number of the purchase order")
    partner_id = fields.Many2one(comodel_name="res.partner.ept", string="Vendor/Supplier")
    warehouse_id = fields.Many2one(string="Warehouse", comodel_name="stock.warehouse.ept")
    order_date=fields.Date(string="Order Date",help="Date of the purchase order",default=fields.Date.today())
    state=fields.Selection([('Draft','Draft'),('Confirmed','Confirmed'),('Done','Done'),('Cancelled','Cancelled')],string="State",help="State of the order",default="Draft")
    purchase_order_line_ids=fields.One2many(comodel_name="purchase.order.line.ept",inverse_name="purchase_order_id",string="Purchase Order line")
    picking_ids = fields.One2many(comodel_name="stock.picking.ept", inverse_name="purchase_order_id", string="Pickings",readonly=True)

    @api.model
    def create(self,vals):
        vals['name'] = self.env['ir.sequence'].next_by_code('my.purchase.order') or 'New'
        return super(PurchaseOrderEpt, self).create(vals)

    @api.multi
    def change_order_state_and_create_picking(self):
        """
        :functionality : Change the order state and create the Stock Picking on order
        :return:
        """
        tmp_stock_moves = []
        source_location = self.env['stock.location.ept'].search([('location_type', '=', 'Vendor')], limit=1)
        if not source_location:
            raise Warning("Vendor cannot be found!.First add the vendor in location")

        for line in self.purchase_order_line_ids:
            name = '{0}: {1} -> {2}'.format(line.product_id.name,source_location.name ,self.warehouse_id.stock_location_id.name)
            tmp_stock_moves.append((0, 0, {'purchase_line_id': line.id,
                                           'name': name, 'product_id': line.product_id.id,
                                           'uom_id': line.uom_id.id,
                                           'source_location_id': source_location.id,
                                           'destination_location_id': self.warehouse_id.stock_location_id.id,
                                           'qty_to_deliver': line.quantity, 'qty_done': 0.0}))
            line.write({'state': 'Confirmed'})

        tmp_stock_picking = self.env['stock.picking.ept'].create({
            'partner_id': self.partner_id.id,
            'purchase_order_id': self.id,
            'transaction_type': 'In',
            'move_ids': tmp_stock_moves})

        self.write({'state': 'Confirmed'})
# -*- conding: utf-8 -*-

from openerp import models,fields,api

class ProductStockUpdate(models.TransientModel):

    _name='product.stock.update.ept'
    _description="Stock Update"

    location_id = fields.Many2one(comodel_name="stock.location.ept", string="Location")
    available_stock = fields.Float(string="Available Stock", help="Available stock of the product")
    counted_qty = fields.Float(string="Counted Quantity", help="Counted Quantity")
    difference_qty = fields.Float(string="Difference", help="difference of product quantity",
                              store=False, compute="compute_difference")

    @api.multi
    def update_stock(self):
        """
        :functionality : Create stock inventory of product
        :return:-
        """
        if self.location_id:
            product_ids = self.env.context.get('active_ids')
            tmp_product= self.env['product.ept'].with_context({'location': self.location_id.id}).browse(product_ids[0])
            tmp_inventry_line=[]
            tmp_inventry_line.append((0,0,{
                'product_id':tmp_product.id,
                'available_qty':tmp_product.product_stock,
                'counted_product_qty':self.counted_qty
            }))
            tmp_inventory=self.env['stock.inventory.ept'].create({
                'name':'{0} - Audit'.format(tmp_product.name),
                'state':'In-progress',
                'location_id':self.location_id.id,
                'inventory_line_ids':tmp_inventry_line
            })
            tmp_inventory.action_validate_inventory()


    @api.depends('counted_qty')
    def compute_difference(self):
        self.difference_qty = (self.counted_qty - self.available_stock)

    @api.onchange('location_id')
    def onchange_location_id(self):
        if self.location_id:
            product_ids=self.env.context.get('active_ids')
            self.available_stock = self.env['product.ept'].\
                with_context({'location': self.location_id.id}).browse(product_ids[0]).product_stock


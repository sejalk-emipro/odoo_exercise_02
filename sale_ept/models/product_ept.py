# -*- coding :utf-8 -*-

from openerp import models,fields,api

class ProductData(models.Model):

    _name="product.ept"
    _description="Product"

    name = fields.Char(string="Name",required=True,help="Name of the product.")
    sku = fields.Char(string="SKU",required=True,help="SKU of the product")
    weight = fields.Float(string="Weight",digits=(16,2),help="Weight of the product")
    length = fields.Float(string="Length",digits=(16,2),help="Length of the product")
    volume = fields.Float(string="volume", digits=(16,2), help="volume of the product")
    width = fields.Float(string="width", digits=(16,2), help="width of the product")
    barcode = fields.Char(string="Barcode",help="Barcode of the product")
    product_type = fields.Selection([('Storable','Storable'),('Consumable','Consumable'),('Service','Service')],string="Product Type")
    sale_price = fields.Float(string="Sale Price", digits=(16,2), help="sale price of the product",default=1.00)
    cost_price = fields.Float(string="Cost Price", digits=(16,2), help="Cost price of the product",default=1.00)
    description = fields.Text(string="Description",help="Description of the product")
    category_id = fields.Many2one(string="Category", comodel_name="product.category.ept")
    uom_id = fields.Many2one(string="UoM",comodel_name="product.uom.ept")
    product_stock=fields.Float(string="Product stock", digits=(16, 2), compute="compute_total_product_stock", store=False,help="Total of the product stock")
    tax_ids=fields.Many2many(comodel_name="account.tax.ept",string="Customer Taxes")


    @api.multi
    def action_update_stock(self):
        action=self.env['ir.actions.act_window'].for_xml_id('sale_ept','update_stock_wizard_action')

        # view=self.env.ref('sale_ept.update_stock_wizard_action')
        # action={
        #     'type':'ir.actions.act_window',
        #     'res_model':'product.stock.update.ept',
        #     'view_type': 'form',
        #     'view_mode': 'form',
        #     'views':[(False,'form')],
        #     'view_id': False,
        #     'target': 'new',
        #     'context': {}
        # }
        return action


    def compute_total_product_stock(self):
        """
        :functionality :Calculate product stock based on moves and locations
        :return: -
        """
        warehouses=self.env['stock.warehouse.ept'].search([])

        # throw Expected singleton: stock.warehouse.ept(3, 4)
        # stock_locations = warehouses.stock_location_id.ids,
        # self.env['stock.warehouse.ept'].search([]).stock_location_id.id

        stock_locations = [self.env.context.get('location')]
        if not self.env.context.get('location'):
            stock_locations = warehouses.mapped(lambda warehouse: warehouse.stock_location_id.id)

        if stock_locations:
            product_stock=0
            for product in self:
                destination_total=0
                source_total=0
                destination_moves=self.env['stock.move.ept'].search([('destination_location_id','in',stock_locations),
                                                                  ('product_id','=',product.id),('state','=','Done')])
                for move in destination_moves:
                    destination_total+=move.qty_to_deliver

                source_stock_moves = self.env['stock.move.ept'].search([('source_location_id', 'in', stock_locations),
                                                                 ('product_id', '=', product.id), ('state', '=', 'Done')])

                for move in source_stock_moves:
                    source_total+=move.qty_to_deliver

                if destination_total>source_total :
                    product_stock=(destination_total-source_total)

                product.product_stock=product_stock


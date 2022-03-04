# -*- coding :utf-8 -*-

from openerp import models,fields,api

class StockInventoryEpt(models.Model):
    _name="stock.inventory.ept"
    _description="Stock Inventory"

    name=fields.Char(string="Name",required=True,help="Name of the stock inventory")
    state=fields.Selection([('Draft','Draft'),('In-progress','In-progress'),('Done','Done'),('cancelled','cancelled')],
                           string="State",default="Draft",help="Sate of the stock inventory")
    location_id = fields.Many2one(comodel_name="stock.location.ept", string="Location",required=True)
    inventory_date=fields.Date(string="Inventory Date",default=fields.Date.today())
    inventory_line_ids=fields.One2many(comodel_name="stock.inventory.line.ept", inverse_name="inventory_id",
                                   string="Inventory Line")
    stock_move_ids=fields.One2many(readonly=True,comodel_name="stock.move.ept",inverse_name="stock_inventory_id",string="Stock Moves")


    @api.multi
    def action_start_inventory(self):
        if self.location_id:
            for line in self.inventory_line_ids:
                line.available_qty=line.product_id.with_context({'location':self.location_id.id}).product_stock

        self.write({'state':'In-progress'})

    @api.multi
    def action_validate_inventory(self):
        inventory_Loss = self.env['stock.location.ept'].search([('location_type', '=', 'Inventory Loss')], limit=1)

        if not inventory_Loss:
            raise Warning("Inventory Loss cannot be found!.First add the Inventory Loss in location")

        for line in self.inventory_line_ids:
            if line.difference!=0:
                positive_diff_location = self.location_id if line.difference > 0 else inventory_Loss
                negative_diff_location = self.location_id if line.difference < 0 else inventory_Loss
                description='{0}: {1} -> {2}'.format(line.product_id.name,positive_diff_location.name,negative_diff_location.name)

                tmp_move=self.env['stock.move.ept'].create({
                     'name':description ,
                     'product_id': line.product_id.id,
                     'uom_id': line.product_id.uom_id.id,
                     'source_location_id': positive_diff_location.id,
                     'destination_location_id': negative_diff_location.id,
                     'qty_to_deliver':abs(line.difference),
                     'qty_done': abs(line.difference),
                     'state': 'Done',
                     'stock_inventory_id':self.id
                })

        self.write({'state':'Done'})

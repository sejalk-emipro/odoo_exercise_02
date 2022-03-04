# -*- coding :utf-8 -*-

from openerp import models,fields,api

class CRMLeadLineEpt(models.Model):

    _name="crm.lead.line.ept"
    _description="CRM Lead Line"

    product_id = fields.Many2one(comodel_name="product.ept", string="product")
    name=fields.Char(string="Description")
    expected_sell_qty=fields.Float(string="Expected sell qty",digits=(16,2))
    uom_id=fields.Many2one(comodel_name="product.uom.ept",string="UoM(Unit of Measurement)")
    lead_id=fields.Many2one(comodel_name="crm.lead.ept",string="Crm Lead")

    @api.onchange('product_id')
    def onchange_product_id(self):
        if self.product_id:
            self.name = self.product_id.description
            if not self.name:
                self.name= self.product_id.name
            self.uom_id=self.product_id.uom_id.id

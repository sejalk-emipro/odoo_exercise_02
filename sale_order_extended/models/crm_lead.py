from openerp import models,fields,api

class CRMLead(models.TransientModel):

    _name="crm.make.sale"
    _inherit="crm.make.sale"

    @api.multi
    def makeOrder(self):
        action=super(CRMLead, self).makeOrder()
        active_ids=self.env.context.get('active_ids')
        sale_order=self.env['sale.order'].browse(action['res_id'])
        crm_lead=self.env['crm.lead'].browse(active_ids[0])
        tag=self.env.ref('sale_order_extended.categ_fromlead')
        sale_order.opportunity_id=crm_lead[0]
        sale_order.categ_ids=crm_lead.categ_ids + tag
        return action




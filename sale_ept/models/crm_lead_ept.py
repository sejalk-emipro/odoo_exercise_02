# -*- coding :utf-8 -*-

from openerp import models,fields,api

class CRMLeadEpt(models.Model):
    _name="crm.lead.ept"
    _description="CRM Lead"

    partner_id=fields.Many2one(comodel_name="res.partner.ept",string="Partner")
    order_ids=fields.One2many(comodel_name="sale.order.ept",inverse_name="crm_lead_id",string="Order",readonly=True)
    team_id = fields.Many2one(comodel_name="crm.team.ept",string="CRM Team")
    user_id=fields.Many2one(comodel_name="res.users",string="Salesperson",required=True)
    lead_line_ids=fields.One2many(comodel_name="crm.lead.line.ept",inverse_name="lead_id",string="CRM Lead Line")
    state=fields.Selection([('New','New'),('Qualified','Qualified'),('Proposition','Proposition'),('Won','Won'),('Lost','Lost')],string="State",help="State of the CRM Lead",default="New")
    won_date=fields.Date(string="Won Date")
    lost_reason=fields.Char(string="Lost Reason",help="Reason of the lost")
    next_followup_date=fields.Date(string="Next Followup Date")
    partner_name=fields.Char(string="Name",help="Name of the partner")
    partner_email=fields.Char(string="Email",help="Email of the partner")
    partner_country_id  = fields.Many2one(comodel_name="res.country.ept", string="Country", help="Country of the customer")
    partner_state_id = fields.Many2one(comodel_name="res.state.ept", string="State", help="State of the country")
    partner_city_id = fields.Many2one(comodel_name="res.city.ept", string="City",help="City of the state")
    partner_phone_no=fields.Char(string="Phone",help="Phone number of the partner")

    @api.model
    def change_qualified_state(self):
        """
        :Functionality: To change state based on button click
        :return: -
        """
        self.write({'state' : 'Qualified'})

    @api.multi
    def change_proposition_state(self):
        self.write({'state': 'Proposition'})

    @api.multi
    def change_won_state(self):
        self.write({'state': 'Won','won_date':fields.Date.today()})


    @api.multi
    def change_lost_state(self):
        self.write({'state': 'Lost'})

    @api.multi
    def generate_sales_quotation(self):
        """
        functionality:generate sales quotation in crm lead using traditional and triplet
        :return: -
        """
        if not self.partner_id:
            raise Warning("Customer cannot be selected, First you have create the customer.")
        else:
            # Traditional way
            order_lines=[]
            for line in self.lead_line_ids:
                order_lines.append((0,0,{'product_id':line.product_id.id,
                                   'name':line.name,'quantity':line.expected_sell_qty,'uom_id':line.uom_id.id,
                                                        'unit_price':line.product_id.sale_price}))

            tmp_order=self.env['sale.order.ept'].new({'partner_id':self.partner_id.id})
            tmp_order.onchange_partner_id()
            order=self.env['sale.order.ept'].create({
                'partner_id':self.partner_id.id,
                'partner_invoice_id':tmp_order.partner_invoice_id.id,
                'partner_shipping_id':tmp_order.partner_shipping_id.id,
                'crm_lead_id':self.id,
                'order_line_ids':order_lines
            })

            # for line in self.lead_line_ids:
            #     self.env['sale.order.line.ept'].create({'order_id':order.id,'product_id':line.product_id.id,
            #                        'name':line.name,'quantity':line.expected_sell_qty,'uom_id':line.uom_id.id,
            #                                             'unit_price':line.product_id.sale_price})


    @api.multi
    def create_partner(self):
        if not self.partner_id:
            partner=self.env['res.partner.ept'].create({'name':self.partner_name,'email':self.partner_email,
                                                               'phone':self.partner_phone_no,'city_id':self.partner_city_id.id,
                                                               'country_id':self.partner_country_id.id,'state_id':self.partner_state_id.id})

            self.write({'partner_id': partner.id})
        else:
            raise Warning("Customer already selected")









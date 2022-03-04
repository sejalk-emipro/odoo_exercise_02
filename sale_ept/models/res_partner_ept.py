# -*- coding :utf-8 -*-

from openerp import models,fields


class Partner(models.Model):

    _name="res.partner.ept"
    _description="Partner"

    name=fields.Char(string="Name",help="Name of the customer")
    street1=fields.Char(string="Street1",help="Address of the customer")
    street2=fields.Char(string="Street2",help="Address of the customer")
    country_id=fields.Many2one(comodel_name="res.country.ept",string="Country",help="Country of the customer")
    state_id=fields.Many2one(comodel_name="res.state.ept",string="State",help="State of the country")
    city_id=fields.Many2one(comodel_name="res.city.ept",string="City")
    zipcode=fields.Char(string="Zip Code")
    email=fields.Char(string="Email",help="Email of the customer")
    phone=fields.Char(string="Phone No",help="Phone number of the customer")
    photo=fields.Binary(string="Image",help="You can add the photo")
    website=fields.Char(string="Website")
    active=fields.Boolean(string="Active",default=True)
    parent_id=fields.Many2one(comodel_name="res.partner.ept",string="Parent")
    child_ids=fields.One2many(comodel_name="res.partner.ept",inverse_name="parent_id",string="Child")
    address_type=fields.Selection([('Invoice','Invoice'),('Shipping','Shipping'),('Contact','Contact')],string="Address Type")


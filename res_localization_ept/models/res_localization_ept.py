# -*- coding :utf-8 -*-

from openerp import models,fields

class CountryData(models.Model):

    _name="res.country.ept"
    _description="Country Demo"

    name=fields.Char(string="Country Name",help="Name  of the country")
    code=fields.Char(string="Country Code",help="Short code of the country")
    state_ids=fields.One2many(comodel_name="res.state.ept",inverse_name="country_id",string="State",help="State")

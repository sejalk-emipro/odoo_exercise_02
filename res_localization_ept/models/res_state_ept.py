# -*- coding :utf-8 -*-

from openerp import models,fields

class StateData(models.Model):

    _name="res.state.ept"
    _description="State Demo"

    name=fields.Char(string="State Name",help="Name of the state")
    code=fields.Char(string="State Code",help="Code of the state")
    country_id=fields.Many2one(comodel_name="res.country.ept",string="Country",help="Name of The Country",copy=False)
    city_ids=fields.One2many(comodel_name="res.city.ept",inverse_name="state_id",string="City",help="Name of the City")
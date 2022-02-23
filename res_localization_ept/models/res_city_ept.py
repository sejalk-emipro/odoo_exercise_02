# -*- coding :utf-8 -*-

from openerp import models,fields

class City(models.Model):

    _name="res.city.ept"
    _description="City Data"

    name=fields.Char(string="City Name",help="Name of the city")
    state_id=fields.Many2one(comodel_name="res.state.ept", string="State", help="Name of the  state",copy=False)


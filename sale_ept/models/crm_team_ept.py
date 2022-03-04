# -*- coding :utf-8 -*-

from openerp import models,fields

class CRMTeamEpt(models.Model):

    _name="crm.team.ept"
    _description="CRM Team"

    name=fields.Char(string="Name", help="Team Name of the CRM")
    team_leader_id=fields.Many2one(comodel_name="res.users",string="Team Leader")

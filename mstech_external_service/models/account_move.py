from odoo import models,fields,api,_
from datetime import timedelta, datetime
from odoo.exceptions import UserError

class AccountMove(models.Model):
    _inherit = 'account.move'
    
    jasatec_os= fields.Char(string='O/S')
    jasatec_constancia= fields.Char(string='Constancia')

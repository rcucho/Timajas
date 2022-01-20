from odoo import models,fields,api,_
from datetime import timedelta, datetime
from odoo.exceptions import UserError

class MaintenanceRequestTimajas(models.Model):
    _inherit = "maintenance.request"
    
    mant_project = fields.One2many('project.task', string="Proyecto")

class ProjectTaskTimajas(models.Model):
    _inherit = "project.task"
    
    proj_mant = fields.Many2one('maintenance.request', string="Peticion de Mantenimiento")

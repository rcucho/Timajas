from odoo import models,fields,api,_
from datetime import timedelta, datetime
from odoo.exceptions import UserError

class MaintenanceRequestTimajas(models.Model):
    _inherit = "maintenance.request"
    
    mant_project = fields.Many2one('project.task', string="Proyecto")
    
    @api.onchange('name')
    def _compute_mant_project(self):
        for record in self:
            #nro = int(record.employee_id.id)
            if record.name:
                record.mant_project = self.env['project.task'].create({
                    'name': record.name,
                    'user_ids' : [(4, record.employee_id.id)],
                    'project_id' : 3,
                })
                #raise UserError(str(type(record.employee_id.id)))
                #raise UserError(_("..."))
    
    
class ProjectTaskTimajas(models.Model):
    _inherit = "project.task"
    
    proj_mant = fields.One2many('maintenance.request','mant_project',string="Peticion de Mantenimiento")

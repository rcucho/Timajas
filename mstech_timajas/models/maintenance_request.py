from odoo import models,fields,api,_
from datetime import timedelta, datetime
from odoo.exceptions import UserError

class MaintenanceRequestTimajas(models.Model):
    _inherit = "maintenance.request"
    
    mant_project = fields.Many2one('project.task', string="Proyecto")
    
    @api.onchange('stage_id')
    def _compute_mant_project(self):
        for record in self:
            if record.stage_id.id == 2:
                record.mant_project = self.env['project.task'].create({
                    'name': record.name,
                    'user_ids' : record.user_id,
                    'project_id' : 3,
                })
class MaintenanceEquipment2(models.Model):
    _inherit = "maintenance.equipment"
    
    eqip_product = fields.Many2one('product.template', string="Producto")
    
    @api.model
    def create(self, vals):
        for record in self:
            eqip_product = self.env['product.template'].create({
                'name': record.name
            })
        equipment = super(MaintenanceEquipment2, self).create(vals)
        return equipment
class ProductTemplate(models.Model):
    _inherit = "product.template"
    
    product_eqip = fields.One2many('maintenance.equipment', 'eqip_product', string="Equipamento de Mantenimiento")
    
class ProjectTaskTimajas(models.Model):
    _inherit = "project.task"
    
    proj_mant = fields.One2many('maintenance.request','mant_project',string="Peticion de Mantenimiento")
    

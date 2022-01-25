from odoo import models,fields,api,_
from odoo.tools.safe_eval import safe_eval
from datetime import timedelta, datetime
from odoo.exceptions import UserError

class MaintenanceRequestTimajas(models.Model):
    _inherit = "maintenance.request"
    #-------------------------------------------------------------------------------------------------------------------
    mant_project = fields.Many2one('project.task', string="Proyecto")
    #-------------------------------------------------------------------------------------------------------------------
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
    #-------------------------------------------------------------------------------------------------------------------
    eqip_product = fields.Many2one('product.product', string="Producto")
    #-------------------------------------------------------------------------------------------------------------------
    eqip_task = fields.One2many('project.task','task_eqip', string="Equipo en Tareas")
    #-------------------------------------------------------------------------------------------------------------------
    @api.model
    def create(self, vals):
        equipment = super(MaintenanceEquipment2, self).create(vals)
        for record in equipment:
            record.eqip_product = self.env['product.product'].create({
                'name': record.name
            })
        return equipment
    
    @api.onchange('maintenance_ids')
    def _compute_eqip_task(self):
        for rec in self:
            rec.eqip_task = rec.maintenance_ids.mant_project
    
class ProductTemplate(models.Model):
    _inherit = "product.product"
    #-------------------------------------------------------------------------------------------------------------------
    product_eqip = fields.One2many('maintenance.equipment', 'eqip_product', string="Equipamento de Mantenimiento")
    project_count = fields.Integer(compute='_compute_project_count', string="Project Count", store= False)
    #-------------------------------------------------------------------------------------------------------------------
    project_pids = fields.Many2many('project.task', compute="_compute_project_ids", string='Projects')
    project_count2 = fields.Integer(compute='_compute_project_ids', string="Project Count")
    #-------------------------------------------------------------------------------------------------------------------    
    @api.depends('stock_move_ids')
    def _compute_project_count(self):
        for record in self:
            qnt_pro = 0
            proj_task = record.project_pids
            for r in proj_task:
                pick = r.task_picking
                move_pro = pick.move_ids_without_package
                for m in move_pro:
                    qnt_pro = qnt_pro + m.quantity_done
            record.project_count = qnt_pro

    @api.depends('product_eqip')
    def _compute_project_ids(self):
        for rec in self:
            projects = rec.product_eqip.mapped('maintenance_ids.mant_project')
            rec.project_pids = projects
            rec.project_count2 = len(projects)
    
    def action_view_project_pids(self):
        self.ensure_one()
        view_form_id = self.env.ref('project.edit_project').id
        view_kanban_id = self.env.ref('project.view_project_kanban').id
        action = {
            'type': 'ir.actions.act_window',
            'domain': [('id', 'in', self.project_pids.ids)],
            'view_mode': 'kanban,form',
            'name': _('Projects'),
            'res_model': 'project.task',
        }
        if len(self.project_pids) == 1:
            action.update({'views': [(view_form_id, 'form')], 'res_id': self.project_pids.id})
        else:
            action['views'] = [(view_kanban_id, 'kanban'), (view_form_id, 'form')]
        return action

    def action_view_task2(self):
        self.ensure_one()
        list_view_id = self.env.ref('project.view_task_tree2').id
        form_view_id = self.env.ref('project.view_task_form2').id

        action = {'type': 'ir.actions.act_window_close'}
        task_projects = self.project_pids.mapped('project_id')
        if len(task_projects) == 1 and len(self.project_pids) > 1:
            action = self.with_context(active_id=task_projects.id).env['ir.actions.actions']._for_xml_id(
                'project.act_project_project_2_project_task_all')
            action['domain'] = [('id', 'in', self.project_pids.ids)]
            if action.get('context'):
                eval_context = self.env['ir.actions.actions']._get_eval_context()
                eval_context.update({'active_id': task_projects.id})
                action_context = safe_eval(action['context'], eval_context)
                action_context.update(eval_context)
                action['context'] = action_context
        else:
            action = self.env["ir.actions.actions"]._for_xml_id("project.action_view_task")
            action['context'] = {}
            if len(self.project_pids) > 1:
                action['views'] = [[False, 'kanban'], [list_view_id, 'tree'], [form_view_id, 'form'], [False, 'graph'], [False, 'calendar'], [False, 'pivot']]
            elif len(self.project_pids) == 1:
                action['views'] = [(form_view_id, 'form')]
                action['res_id'] = self.project_pids.id
        action.setdefault('context', {})
        return action
                
class ProductTemplate(models.Model):
    _inherit = "product.template"
    
    product_eqip_temp = fields.One2many(string="Equipamento de Mantenimiento", related='product_variant_id.product_eqip')
    project_count_temp = fields.Integer(string="Project Count", related='product_variant_id.project_count')
        
class ProjectTaskTimajas(models.Model):
    _inherit = "project.task"
    
    proj_mant = fields.One2many('maintenance.request','mant_project',string="Peticion de Mantenimiento")
    

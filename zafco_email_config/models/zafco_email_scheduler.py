# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import _, api, fields, models

class ZafcoEmailScheduler(models.Model):
    _name = "zafco.email.scheduler"
    _description = "List dashboard to auto email in scheduler"
    
    partner_id = fields.Many2one('res.partner', string='Contacts', required=True, domain=[('email', '!=', False)])
    partner_email = fields.Char(compute='_compute_partner_email', string='Partner Email')
    
    dashboard_ids = fields.Many2many('izi.dashboard', string='Dashboard')
    is_active = fields.Boolean('Active', default=True)


    @api.depends('partner_id')
    def _compute_partner_email(self):
        for rec in self:
            rec.partner_email = rec.partner_id.email

    @api.depends('partner_id')
    def _compute_display_name(self):
        for rec in self:
            rec.display_name = rec.partner_id.name 

    def _process_send_email(self):
        config = self.env.ref('zafco_email_config.default_email_config')
        expiration_hour = config.expiration_hour
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        schedulers = self.env['zafco.email.scheduler'].search([('is_active','=',True)])

        for scheduler in schedulers:
            email = scheduler.partner_id.email
            links = []
            for dashboard in scheduler.dashboard_ids:
                token = dashboard.generate_access_token({},expiration_hour=expiration_hour)
                if token:
                    links.append(f"{base_url}/izi/dashboard/{dashboard.id}/page?access_token={token}")

            template = self.env.ref('zafco_email_config.mail_template_dashboard_reminder')
        
            email_context = {
                'links': links,
                'email_from': self.env.user.email or 'default@example.com',
                'email_to': email,
            }
            template.with_context(email_context).send_mail(scheduler.id, force_send=True)
        
        return True

class ZafcoEmailConfig(models.Model):
    _name = "zafco.email.config"
    _description = "Config for email scheduler"
    
    expiration_hour = fields.Integer('Expiration Token (Hour)', default=1)

    def _compute_display_name(self):
        for rec in self:
            rec.display_name = "Email Scheduler Config"
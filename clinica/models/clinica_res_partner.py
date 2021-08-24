# -*- coding: utf-8 -*-


from datetime import datetime

from dateutil.relativedelta import relativedelta

from odoo import models, fields, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    fdn = fields.Date('Fecha de Nacimiento')
    sex = fields.Selection([
        ('H', 'Hombre'),
        ('M', 'Mujer')
    ], string="Sexo")
    lpd = fields.Boolean(string="Ley de Protección de Datos", default=False)
    pare = fields.Char(string="Parentesco")
    edad = fields.Char(compute="calc_edad", string="Edad", readonly=True, store=True)

    servicios_ids = fields.One2many('res.partner.servicios', 'partner_id')
    count_servs = fields.Integer(compute='_compute_count_servs', string="Datos Servicios")

    attachment_ids = fields.One2many('ir.attachment', 'partner_id')
    count_doct = fields.Integer(compute='_compute_count_doct', string="Document Count")

    @api.depends("fdn")
    def calc_edad(self):
        for rec in self:
            if rec.fdn:
                d1 = rec.fdn
                d2 = datetime.today().date()
                rd = relativedelta(d2, d1)
                # rec.edad = str(rd.years) + "a" + " " + str(rd.months) + "m" + " " + str(rd.days) + "d"
                rec.edad = str(rd.years) + "a"
            else:
                rec.edad = "Sin fecha de nacimiento!!"

    def _compute_count_doct(self):
        for partner in self:
            partner.count_doct = len(partner.attachment_ids.ids)

    def action_get_attachment_tree_view(self):
        action = self.env.ref('base.action_attachment').read()[0]
        action['name'] = "Documents"
        action['domain'] = [('partner_id', '=', self.id)]
        action['context'] = {'default_partner_id': self.id}
        return action

    def _compute_count_servs(self):
        for partner in self:
            partner.count_servs = len(partner.servicios_ids.ids)

    def action_get_servicios_tree_view(self):
        action = self.env.ref('clinica.action_servicios').read()[0]
        action['name'] = "Services"
        action['domain'] = [('partner_id', '=', self.id)]
        action['context'] = {'default_partner_id': self.id}
        return action

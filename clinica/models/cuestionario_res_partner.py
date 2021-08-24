# -*- coding: utf-8 -*-
from odoo import fields, models, api
from datetime import date, datetime


class CuestResPartner(models.Model):
    _description = 'Cuestionario'
    _name = "res.partner.cuestionario"
    _rec_name = 'partner_id'

    partner_id = fields.Many2one('res.partner', 'Paciente', required=True)
    fecha_reg = fields.Date('Fecha', default=datetime.today().date())
    edad = fields.Char('Edad', stored=True, related='partner_id.edad')
    sexo = fields.Selection('Sexo', stored=True, related='partner_id.sex')

    hc01 = fields.Selection([('si', 'Si'), ('no', 'No')], string='Si/No')
    hc01_comen = fields.Text(string="Comentarios")
    hc02 = fields.Selection([('si', 'Si'), ('no', 'No')], string='Si/No')
    hc02_comen = fields.Text(string="Comentarios")
    hc03 = fields.Selection([('si', 'Si'), ('no', 'No')], string='Si/No')
    hc03_comen = fields.Text(string="Comentarios")
    hc04 = fields.Selection([('si', 'Si'), ('no', 'No')], string='Si/No')
    hc04_comen = fields.Text(string="Comentarios")
    hc05 = fields.Selection([('si', 'Si'), ('no', 'No')], string='Si/No')
    hc05_comen = fields.Text(string="Comentarios")
    hc06 = fields.Selection([('si', 'Si'), ('no', 'No')], string='Si/No')
    hc06_comen = fields.Text(string="Comentarios")
    hc07 = fields.Selection([('si', 'Si'), ('no', 'No')], string='Si/No')
    hc07_comen = fields.Text(string="Comentarios")
    hc08_comen = fields.Text(string="Comentarios")
    hc09 = fields.Selection([('si', 'Si'), ('no', 'No')], string='Si/No')
    hc09_comen = fields.Text(string="Comentarios")
    hc10 = fields.Selection([('si', 'Si'), ('no', 'No')], string='Si/No')
    hc10_comen = fields.Text(string="Comentarios")



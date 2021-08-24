# -*- coding: utf-8 -*-

import math
from datetime import datetime, date

from dateutil.relativedelta import relativedelta

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class ResPartner(models.Model):
    _inherit = 'res.partner'

    fdn = fields.Date('Fecha de Nacimiento')
    edad = fields.Char(compute="calc_edad", string="Edad", readonly=True, store=True)
    age = fields.Integer(compute="calc_edad", store=True)
    fecha_alta = fields.Date('Fecha de Alta')
    fecha_baja = fields.Date('Fecha de Baja')
    num_colegiado = fields.Char('Número de colegiado')
    estado = fields.Selection([
        ('1', 'Jubilado'),
        ('2', 'Desempleado'),
        ('3', 'Exento')],
        string="Estado del colegiado")
    metodo_pago = fields.Selection([
        ('DB', 'Domiciliación Bancaria'),
        ('ST', 'S/ Transferencia'),
        ('EF', 'Efectivo')],
        string="Método de Pago")

    # contact_m2m_ids = fields.Many2many(
    #     "res.partner",
    #     "rel_table",
    #     "direct_rel_id",
    #     "back_rel_id",
    #     string="Contacts"
    # )
    # parents_m2m_ids = fields.Many2many(
    #     "res.partner",
    #     "rel_table",
    #     "back_rel_id",
    #     "direct_rel_id",
    #     string="Companies"
    # )

    @api.depends("fdn")
    def calc_edad(self):
        for rec in self:
            if rec.fdn:
                d1 = rec.fdn
                d2 = datetime.today().date()
                rd = relativedelta(d2, d1)
                rec.edad = str(rd.years) + "a"
                rec.age = rd.years
            else:
                rec.edad = "Sin fecha de nacimiento!!"
                rec.age = 0

    @api.onchange('fdn', 'estado')
    def onchange_customer_pricelist(self):
        pls = self.env['product.pricelist'].search([], order='id asc')
        for rec in self:
            if rec.fdn or rec.estado:
                if rec.age > 65 or rec.estado == '1':
                    rec.property_product_pricelist = pls[1]
                elif rec.estado == '2':
                    rec.property_product_pricelist = pls[2]
                elif rec.estado == '3':
                    rec.property_product_pricelist = pls[4]
                elif rec.age < 28:
                    rec.property_product_pricelist = pls[3]
                else:
                    rec.property_product_pricelist = pls[5]
            else:
                rec.property_product_pricelist = pls[0]

    @api.constrains('fecha_alta', 'fecha_baja')
    def check_fecha_fin(self):
        if self.fecha_alta and self.fecha_baja:
            if self.fecha_baja < self.fecha_alta:
                raise ValidationError(
                    _('La fecha de baja no puede ser anterior a la fecha de alta.')
                )


# class ContractAbstract(models.AbstractModel):
#     _inherit = 'contract.abstract.contract'
#
#     numcole = fields.Char(related='partner_id.num_colegiado')
#     pricelist_id = default = lambda self: self.env['res.partner'].search(
#         [('parent_id', '=', False), ('num_colegiado', '=', numcole)], limit=1).mapped('property_product_pricelist').id


class ContractLine(models.AbstractModel):
    _inherit = 'contract.abstract.contract.line'

    is_prorate = fields.Boolean(string="¿Precio Proporcional?", default=True)


class Contract(models.Model):
    _inherit = 'contract.contract'

    falta = fields.Date(related='partner_id.fecha_alta')
    numcol = fields.Char(related='partner_id.num_colegiado')

    @api.onchange('partner_id')
    def onchange_contract_pricelist(self):
        partner_plist = self.env['res.partner'].search([('parent_id', '=', False), ('num_colegiado', '=', self.numcol)], limit=1)
        if partner_plist:
            self.pricelist_id = partner_plist.property_product_pricelist
        else:
            raise ValidationError(
                _("El colegiado no tiene nùmero de colegiado")
            )


class ContractLine(models.Model):
    _inherit = 'contract.line'

    @api.multi
    def _prepare_invoice_line(self, invoice_id=False, invoice_values=False):
        partner_dates = self.env['contract.contract'].search([('id', '=', self.contract_id.id)], limit=1)
        if partner_dates.falta:
            dateMonthStart = date(year=partner_dates.recurring_next_date.year,
                                  month=((math.floor(
                                      ((partner_dates.recurring_next_date.month - 1) / 4) + 1) - 1) * 4) + 1, day=1)
            dateMonthEnd = (dateMonthStart + relativedelta(months=4))
            dateMonthFin = (dateMonthStart + relativedelta(months=4, days=-1))
            rangePeriod = abs(dateMonthEnd - dateMonthStart).days
            dateDiff = abs(dateMonthFin - partner_dates.falta).days
            if partner_dates.falta <= dateMonthStart:
                pre_u = self.price_unit
            else:
                pre_u = self.price_unit / rangePeriod * dateDiff
        else:
            raise ValidationError(
                _("El colegiado no tiene Fecha de Alta")
            )
        dates = self._get_period_to_invoice(self.last_date_invoiced, self.recurring_next_date)
        invoice_line_vals = {
            'display_type': self.display_type,
            'product_id': self.product_id.id,
            'quantity': self._get_quantity_to_invoice(*dates),
            'uom_id': self.uom_id.id,
            'discount': self.discount,
            'contract_line_id': self.id,
        }
        if invoice_id:
            invoice_line_vals['invoice_id'] = invoice_id.id
        invoice_line = self.env['account.invoice.line'].with_context(
            force_company=self.contract_id.company_id.id,
        ).new(invoice_line_vals)
        if invoice_values and not invoice_id:
            invoice = self.env['account.invoice'].with_context(
                force_company=self.contract_id.company_id.id,
            ).new(invoice_values)
            invoice_line.invoice_id = invoice
        # Get other invoice line values from product onchange
        invoice_line._onchange_product_id()
        invoice_line_vals = invoice_line._convert_to_write(invoice_line._cache)
        # Insert markers
        name = self._insert_markers(dates[0], dates[1])
        if self.is_prorate:
            invoice_line_vals.update(
                {
                    'sequence': self.sequence,
                    'name': name,
                    'account_analytic_id': self.analytic_account_id.id,
                    'analytic_tag_ids': [(6, 0, self.analytic_tag_ids.ids)],
                    'price_unit': pre_u,
                }
            )
        else:
            invoice_line_vals.update(
                {
                    'sequence': self.sequence,
                    'name': name,
                    'account_analytic_id': self.analytic_account_id.id,
                    'analytic_tag_ids': [(6, 0, self.analytic_tag_ids.ids)],
                    'price_unit': self.price_unit,
                }
            )
        return invoice_line_vals

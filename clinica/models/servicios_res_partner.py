# -*- coding: utf-8 -*-
from datetime import datetime

from odoo import fields, models


class ServResPartner(models.Model):
    _description = 'Formularios de Servicios'
    _name = 'res.partner.servicios'
    _rec_name = 'partner_id'

    def _default_services(self):
        return self.env['res.partner.utils'].browse(self._context.get('servs_id'))

    # def _default_subservices(self):
    #     return self.env['res.partner.utils'].browse(self._context.get('subservs_id'))

    partner_id = fields.Many2one('res.partner', 'Paciente', required=True)
    fecha_reg = fields.Date('Fecha', default=datetime.today().date())
    edad = fields.Char('Edad', stored=True, related='partner_id.edad')
    sexo = fields.Selection('Sexo', stored=True, related='partner_id.sex')

    # servs_id = fields.Many2many('res.partner.utils', column1='partner_id', column2='servs_id', string='Servicios',
    #                               default=_default_services)

    servicios = fields.Selection([('co', 'Corporal'),
                                  ('fa', 'Facial'),
                                  ('de', 'Depilación'),
                                  ('fo', 'Fisioterapia/Osteopatia'),
                                  ('nu', 'Nutrición'),
                                  ('we', 'Wellness')], string="Servicios", required=True)

    # corporal = fields.Boolean(string='Corporal')
    # facial = fields.Boolean(string='Facial')
    # depilacion = fields.Boolean(string='Depilación')
    # fisio_osteo = fields.Boolean(string='Fisioterapia/Osteopatia')
    # nutricion = fields.Boolean(string='Nutrición')
    # welness = fields.Boolean(string='Wellness')

    adjunto_ids = fields.One2many('ir.attachment', 'adjunto_id')

    # //-*- HISTORIA CLINICA -*-//
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

    # //-*- ESTUDIO CORPORAL/FACIAL -*-//
    objetivo = fields.Text('Objetivo:')
    sol = fields.Selection([('si', 'Si'), ('no', 'No')], string='Sol')
    tabaco = fields.Selection([('si', 'Si'), ('no', 'No')], string='Tabaco')
    alcohol = fields.Selection([('si', 'Si'), ('no', 'No')], string='Alcohol')
    alimentacion = fields.Selection([('si', 'Si'), ('no', 'No')], string='Alimentación')
    enfermedades = fields.Selection([('si', 'Si'), ('no', 'No')], string='Enfermedades')
    medicamentos = fields.Selection([('si', 'Si'), ('no', 'No')], string='Medicamentos')
    tratamiento = fields.Selection([('si', 'Si'), ('no', 'No')], string='Tratamiento')
    embarazo = fields.Selection([('si', 'Si'), ('no', 'No')], string='Embarazo/Lactancia')
    tra_estetico = fields.Selection([('si', 'Si'), ('no', 'No')], string='Tratamientos Estéticos')
    tra_medicos = fields.Selection([('si', 'Si'), ('no', 'No')], string='Tratamientos Médicos')
    mala_digest = fields.Selection([('si', 'Si'), ('no', 'No')], string='Mala Digestión')
    alergias = fields.Selection([('si', 'Si'), ('no', 'No')], string='Alergias')
    hijos = fields.Selection([('si', 'Si'), ('no', 'No')], string='Hijos(as)')
    observacion = fields.Text('Observaciónes')

    # -*- Cuidados en casa -*-
    higiene = fields.Text('Higiene')
    dia = fields.Text('Dia')
    noche = fields.Text('Noche')
    semanal = fields.Text('Semanal')
    mensual = fields.Text('Mensual')

    # -*- Percepción facial/corporal del profesional -*-
    acne = fields.Boolean('Acné')
    grasa = fields.Boolean('Grasa')
    mancha = fields.Boolean('Mancha')
    sequedad = fields.Boolean('Sequedad')
    eccema = fields.Boolean('Eccema')
    tirantez = fields.Boolean('Tirantez')
    comedones = fields.Boolean('Comedones')
    arruga = fields.Boolean('Arruga')
    flacidez = fields.Boolean('Flacidez')
    desvitavilidad = fields.Boolean('Desvitavilidad')
    rojez = fields.Boolean('Rojez')
    sensibilidad = fields.Boolean('Sensibilidad')
    circulacion = fields.Boolean('Circulación')
    pesadez = fields.Boolean('Pesadez')
    celulitis = fields.Boolean('Celulitis')
    sobrepeso = fields.Boolean('Sobrepeso')
    grasa_loca = fields.Boolean('Grasa Localizada')
    hormigueo = fields.Boolean('Hormigueo')
    comentarios = fields.Text('Descripción por zonas')

    # -*- Datos del analizador -*-
    hidratacion = fields.Char('Hidratación:')
    elasticidad = fields.Char('Elasticidad:')
    manchass = fields.Char('Manchas:')
    grasas = fields.Char('Grasa:')

    # -*- Datos de resultados -*-
    anual = fields.Char('Anual:')
    trat_ase = fields.Text('Tratamiento asesorado:')
    prod_ase = fields.Char('Producto asesorado:')
    dedia = fields.Text('Día:')
    denoche = fields.Text('Noche:')
    muestras = fields.Text('Muestras:')
    observ = fields.Text('Observaciones:')

    # -*- Datos de servicios -*-
    servicios_ids = fields.One2many('res.service.utils', 'tratamientos_id')

    # //-*- FISIOTERAPIA/OSTEOPATIA/NUTRICIÓN/WELLNESS -*-//
    peso = fields.Float('Peso')
    estatura = fields.Float('Estatura')

    diabetes = fields.Selection([('si', 'Si'), ('no', 'No')], string='Diabetes')
    colesterol = fields.Selection([('si', 'Si'), ('no', 'No')], string='Colesterol')
    sobrepesso = fields.Selection([('si', 'Si'), ('no', 'No')], string='Sobrepeso')
    hipertension = fields.Selection([('si', 'Si'), ('no', 'No')], string='Hipertensión')
    enf_hepaticas = fields.Selection([('si', 'Si'), ('no', 'No')], string='Enfermedades Hepáticas')
    enf_cardiacas = fields.Selection([('si', 'Si'), ('no', 'No')], string='Enfermedades Cardiacas')
    enf_apa_diges = fields.Selection([('si', 'Si'), ('no', 'No')], string='Efermedades Aparato Digestivo')
    enf_respirato = fields.Selection([('si', 'Si'), ('no', 'No')], string='Enfermedades Respiratorias')
    enf_osteartic = fields.Selection([('si', 'Si'), ('no', 'No')], string='Enfermedades Osteoarticulares')
    afe_hormanale = fields.Selection([('si', 'Si'), ('no', 'No')], string='Afectaciones Hormonales')
    acc_cereb_vas = fields.Selection([('si', 'Si'), ('no', 'No')], string='Accidentes Cerebro Vasculares')
    epi_afec_cuta = fields.Selection([('si', 'Si'), ('no', 'No')], string='Epilepsia/Afecciones Cutáneas')
    trastor_sueno = fields.Selection([('si', 'Si'), ('no', 'No')], string='Trastorno de Sueño')
    depresion = fields.Selection([('si', 'Si'), ('no', 'No')], string='Depresión')
    ansiedad = fields.Selection([('si', 'Si'), ('no', 'No')], string='Ansiedad')

    analit_rec = fields.Selection([('si', 'Si'), ('no', 'No')], string='Analitica Reciente')

    res_cap_car = fields.Selection([('un', '1'), ('do', '2'), ('tr', '3'), ('cu', '4'), ('ci', '5')],
                                   string='Resistencia y capacidad cardiorrespiratoria')
    fur_res_mus = fields.Selection([('un', '1'), ('do', '2'), ('tr', '3'), ('cu', '4'), ('ci', '5')],
                                   string='Fuerza y resistencia muscular')
    flexibilidad = fields.Selection([('un', '1'), ('do', '2'), ('tr', '3'), ('cu', '4'), ('ci', '5')],
                                    string='Flexibilidad')
    agili_coordi = fields.Selection([('un', '1'), ('do', '2'), ('tr', '3'), ('cu', '4'), ('ci', '5')],
                                    string='Agilidad y coordinación')

    # -*- Nutricion -*-
    nu01 = fields.Selection([('si', 'Si'), ('no', 'No')], string='Si/No')
    nu01_comen = fields.Text(string="Comentarios")
    nu02 = fields.Selection([('si', 'Si'), ('no', 'No')], string='Si/No')
    nu02_comen = fields.Text(string="Comentarios")
    nu03 = fields.Selection([('si', 'Si'), ('no', 'No')], string='Si/No')
    nu03_comen = fields.Text(string="Comentarios")

    # -*- Fisioterapia / Osteopatía -*-
    fo01 = fields.Selection([('si', 'Si'), ('no', 'No')], string='Si/No')
    fo01_comen = fields.Text(string="Comentarios")
    fo02 = fields.Selection([('si', 'Si'), ('no', 'No')], string='Si/No')
    fo02_comen = fields.Text(string="Comentarios")
    fo03 = fields.Selection([('si', 'Si'), ('no', 'No')], string='Si/No')
    fo03_comen = fields.Text(string="Comentarios")
    fo04 = fields.Selection([('si', 'Si'), ('no', 'No')], string='Si/No')
    fo04_comen = fields.Text(string="Comentarios")
    fo05 = fields.Selection([('si', 'Si'), ('no', 'No')], string='Si/No')
    fo05_comen = fields.Text(string="Comentarios")

    # -*- Wellness -*-
    we01 = fields.Selection([('si', 'Si'), ('no', 'No')], string='Si/No')
    we01_comen = fields.Text(string="Comentarios")
    we02 = fields.Selection([('si', 'Si'), ('no', 'No')], string='Si/No')
    we02_comen = fields.Text(string="Comentarios")
    we03 = fields.Selection([('si', 'Si'), ('no', 'No')], string='Si/No')
    we03_comen = fields.Text(string="Comentarios")

    # //-*- DEPILACION LASER -*-//
    dp01 = fields.Selection([('si', 'Si'), ('no', 'No')], string='Si/No')
    dp01_comen = fields.Text(string="Comentarios")
    dp02 = fields.Selection([('si', 'Si'), ('no', 'No')], string='Si/No')
    dp02_comen = fields.Text(string="Comentarios")
    dp03 = fields.Selection([('si', 'Si'), ('no', 'No')], string='Si/No')
    dp03_comen = fields.Text(string="Comentarios")
    dp04 = fields.Selection([('si', 'Si'), ('no', 'No')], string='Si/No')
    dp04_comen = fields.Text(string="Comentarios")

    ult_sis_dep = fields.Selection([('ce', 'Cera'), ('af', 'Afeitado'), ('cr', 'Crema'), ('el', 'Electrica')],
                                   string='Si/No')
    tiemp_trans = fields.Char('Tiempo transcurrido desde la última sesión:')
    utima_expos = fields.Char('Última exposición al sol:')
    areas_trata = fields.Char('Áreas del tratamiento:')

    color_vello = fields.Selection([('ne', 'Negro'), ('ca', 'Castaño'), ('pr', 'Pelirrojo'), ('ru', 'Rubio'), ('cl', 'Claro')], string='Color del Vello')
    grosor = fields.Selection([('gr', 'Grueso'), ('me', 'Medio'), ('fi', 'Fino'), ('ve', 'Vello')], string="Grosor")
    dens_peli = fields.Selection([('al', 'Alta'), ('md', 'Media'), ('ba', 'Baja')], string='Densidad Pilífera')
    tolerancia = fields.Selection([('bn', 'Buena'), ('re', 'Regular'), ('nt', 'No tolera')], string='Tolerancia')
    tono_piel = fields.Selection([('cl', 'Claro'), ('md', 'Medio'), ('os', 'Oscuro')], string='Tono de Piel')
    observs = fields.Text('Observaciones')

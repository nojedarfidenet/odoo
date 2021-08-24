# -*- coding: utf-8 -*-
{
    'name': "Clinica",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "Fidenet",
    'website': "http://www.fidenet.net",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'web', 'mail'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/res_partner_clinica_views.xml',
        'views/res_partner_doct_view.xml',
        'views/res_partner_serv_view.xml',
        'views/res_partner_utils_view.xml',
        'views/ir_attach.xml',
        'views/resource.xml',
        'views/ks_preview_templates.xml',
        'data/clinica_mercadeo.xml',
        'data/clinica_servicios.xml',
        #'data/clinica_servs.xml',
    ],
    'qweb': [
        'static/src/xml/ks_binary_preview.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'installable': True,
    'auto_install': False
}

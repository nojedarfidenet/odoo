# -*- coding: utf-8 -*-
{
    'name': "Citas Timeline",
    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "Fidenet",
    'website': "http://www.fidenet.net",
    "category": "Uncategorized",
    'version': '0.1',
    'depends': ['web'],
    'qweb': [
        'static/src/xml/cits_timeline.xml',
    ],
    'data': [
        'views/cits_timeline_template.xml',
    ],
}

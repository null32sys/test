# -*- coding: utf-8 -*-
{
    'name': "Work Diary",

    'summary': """
        Work Diary""",

    'description': """
        Work Diary
    """,

    'author': "Hashmicro/Wangoes Technology/Pooja",
    'website': "http://www.hashmicro.com",

    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','report'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'security/security.xml',
        'views/views.xml',
        'views/congfiguration.xml',
        'views/submission_report.xml',
        'views/templates.xml',
    ],
}
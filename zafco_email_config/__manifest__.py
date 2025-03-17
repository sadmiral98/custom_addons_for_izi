# -*- coding: utf-8 -*-
{
    "name": "Zafco Email Config",
    'version': '17.0.1.0.3',
    "category": "Customize",
    "summary": "Zafco Email Config",
    "description": """
    Zafco Email Config.
    """,
    "author": "IZI PT Solusi Usaha Mudah",
    "support": "admin@iziapp.id",
    # "website": "https://iziapp.id",
    "license": "OPL-1",
    "maintainer": "RIZKY",
    "depends": ["base","izi_dashboard"],
    "data": [
        'security/ir.model.access.csv',
        'data/ir_cron.xml',
        'data/data.xml',
        # 'views/res_company.xml',
        'views/email_scheduler_view.xml',
    ],
    'assets': {
    },
    "images": [],
    "qweb": [
    ],
    "installable": True,
    "auto_install": False,
    "application": True,
}

# -*- coding: utf-8 -*-
# Copyright (c) 2012 Geoff Wilson <gmwils@gmail.com>

from cihui import handler

import os
import tornado.web


class CiHuiApplication(tornado.web.Application):
    def __init__(self, data_layer, cookie_secret=None):
        self.db = data_layer

        settings = {'static_path': os.path.join(os.path.dirname(__file__), '../static'),
                    'template_path': os.path.join(os.path.dirname(__file__), '../templates'),
                    'xsrf_cookies': True
                    }

        if cookie_secret is None:
            settings['cookie_secret'] = 'Crouching Tiger, Hidden Dragon'
        else:
            settings['cookie_secret'] = cookie_secret

        handlers = [(r'/', handler.MainHandler, dict(database=self.db)),
                    (r'/list/([0-9]+).*', handler.WordListHandler, dict(database=self.db)),
                    (r'/api/account', handler.APIAccountHandler, dict(database=self.db)),
                    (r'/api/list', handler.APIListHandler, dict(database=self.db)),
                    ]

        tornado.web.Application.__init__(self, handlers, **settings)

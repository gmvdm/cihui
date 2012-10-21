# -*- coding: utf-8 -*-
# Copyright (c) 2012 Geoff Wilson <gmwils@gmail.com>

from cihui import handler

import tornado.web


class CiHuiApplication(tornado.web.Application):
    def __init__(self, data_layer):
        self.db = data_layer

        handlers = [
            (r'/', handler.MainHandler, dict(database=self.db)),
            (r'/api/word', handler.APIWordHandler, dict(database=self.db))
            ]

        tornado.web.Application.__init__(self, handlers)

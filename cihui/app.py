# -*- coding: utf-8 -*-
# Copyright (c) 2012 Geoff Wilson <gmwils@gmail.com>

from cihui import handler

import tornado.web


class CiHuiApplication(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r'/', handler.MainHandler),
            (r'/api/word', handler.APIWordHandler)
            ]

        tornado.web.Application.__init__(self, handlers)

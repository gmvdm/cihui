# -*- coding: utf-8 -*-
# Copyright (c) 2012 Geoff Wilson <gmwils@gmail.com>

import tornado.web

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write(u"你好，世界!")

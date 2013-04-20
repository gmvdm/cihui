#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2013 Geoff Wilson <gmwils@gmail.com>

from cihui import app, data
from selenium import webdriver
from threading import Thread

import os
import sys
import tornado.ioloop
import unittest


class Server(Thread):
    def __init__(self, app):
        self.app = app
        Thread.__init__(self)

    def run(self):
        self.app.listen(5555)
        tornado.ioloop.IOLoop.instance().start()


class TestHomepage(unittest.TestCase):
    def setUp(self):
        db_url = os.environ.get('DATABASE_URL', 'postgresql://localhost:5432/cihui')
        self.application = app.CiHuiApplication(data.AccountData(db_url),
                                                data.ListData(db_url),
                                                os.environ.get('COOKIE_SECRET', None),
                                                debug=False)

        self.server = Server(self.application)
        self.server.start()
        self.browser = webdriver.Firefox()

    def tearDown(self):
        tornado.ioloop.IOLoop.instance().stop()
        self.browser.close()

    def testTitle(self):
        self.browser.get('http://localhost:5555/')
        self.assertIn('CiHui', self.browser.title)


if __name__ == '__main__':
    unittest.main(verbosity=2)

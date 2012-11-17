# -*- coding: utf-8 -*-
# Copyright (c) 2012 Geoff Wilson <gmwils@gmail.com>

import unittest

from tornado.testing import AsyncHTTPTestCase
from cihui import app


class Data:
    def get_lists(self, callback):
        callback([{'id': 123, 'title': 'list123'}])


class DisplayWordListsTest(AsyncHTTPTestCase):

    def get_app(self):
        self.db = Data()
        return app.CiHuiApplication(self.db)

    def setUp(self):
        AsyncHTTPTestCase.setUp(self)

    def test_show_homepage(self):
        self.http_client.fetch(self.get_url('/'), self.stop)
        response = self.wait()

        self.assertEqual(200, response.code)
        self.assertIn('list123', response.body)

    def test_invalid_url(self):
        self.http_client.fetch(self.get_url('/fish'), self.stop)
        response = self.wait()

        self.assertEqual(404, response.code)


if __name__ == '__main__':
    unittest.main()

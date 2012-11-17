# -*- coding: utf-8 -*-
# Copyright (c) 2012 Geoff Wilson <gmwils@gmail.com>

import unittest

from tornado.testing import AsyncHTTPTestCase
from cihui import app


class Data:
    def get_word_list(self, list_id, callback):
        if list_id != 404:
            callback({'id': list_id, 'title': 'list_%d' % list_id})
        else:
            callback(None)


class DisplayWordListTest(AsyncHTTPTestCase):

    def get_app(self):
        self.db = Data()
        return app.CiHuiApplication(self.db)

    def setUp(self):
        AsyncHTTPTestCase.setUp(self)

    def test_show_word_list(self):
        self.http_client.fetch(self.get_url('/list/123'), self.stop)
        response = self.wait()

        self.assertEqual(200, response.code)
        self.assertIn('list_123', response.body)

    def test_missing_list(self):
        self.http_client.fetch(self.get_url('/list/404'), self.stop)
        response = self.wait()

        self.assertEqual(404, response.code)


if __name__ == '__main__':
    unittest.main()

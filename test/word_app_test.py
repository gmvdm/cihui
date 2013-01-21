# -*- coding: utf-8 -*-
# Copyright (c) 2012 Geoff Wilson <gmwils@gmail.com>

import unittest

from tornado.testing import AsyncHTTPTestCase
from cihui import app


class Data:
    def get_word_list(self, list_id, callback):
        if list_id not in [404]:
            words = [[u'大', 'da', ['big']], ]
            callback({'id': list_id, 'title': 'list_%d' % list_id, 'words': words})
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

    def test_descriptive_stub(self):
        self.http_client.fetch(self.get_url('/list/101-some-great-list'), self.stop)
        response = self.wait()

        self.assertEqual(200, response.code)

    def test_csv_output(self):
        self.http_client.fetch(self.get_url('/list/102.csv'), self.stop)
        response = self.wait()

        self.assertEqual(200, response.code)
        self.assertIn('text/csv', response.headers['Content-Type'])
        self.assertIn('big', response.body)


if __name__ == '__main__':
    unittest.main()

# -*- coding: utf-8 -*-
# Copyright (c) 2012 Geoff Wilson <gmwils@gmail.com>

import mock
import os
import support
import unittest

from cihui import handler

from tornado.testing import AsyncHTTPTestCase


class DisplayWordListTest(support.HandlerTestCase):
    def setUp(self):
        class ListData:
            def get_word_list(self, list_id, callback):
                if list_id not in [404]:
                    words = [[u'大', 'da', ['big']], ]
                    callback({'id': list_id,
                              'title': 'list_%d' % list_id,
                              'words': words})
                else:
                    callback(None)

        self.list_db = ListData()

        AsyncHTTPTestCase.setUp(self)

    def get_handlers(self):
        return [(r'/list/([0-9]+)[^\.]*(\.?\w*)',
                 handler.WordListHandler,
                 dict(list_db=self.list_db))]

    def get_app_kwargs(self):
        return {'static_path': os.path.join(os.path.dirname(__file__), '../static'),
                'template_path': os.path.join(os.path.dirname(__file__), '../templates')}

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

# -*- coding: utf-8 -*-
# Copyright (c) 2012 Geoff Wilson <gmwils@gmail.com>

import mock
import unittest

from tornado.testing import AsyncHTTPTestCase
from cihui import app


class ListData:
    def get_lists(self, callback):
        callback([{'id': 123, 'title': 'list123', 'stub': 'test-stub'}])


class DisplayWordListsTest(AsyncHTTPTestCase):
    def get_app(self):
        self.account_db = mock.Mock()
        self.list_db = ListData()
        return app.CiHuiApplication(self.account_db, self.list_db)

    def setUp(self):
        AsyncHTTPTestCase.setUp(self)

    def test_show_homepage(self):
        self.http_client.fetch(self.get_url('/'), self.stop)
        response = self.wait()

        self.assertEqual(200, response.code)
        self.assertIn('list123', response.body)
        self.assertIn('123-test-stub', response.body)

    def test_invalid_url(self):
        self.http_client.fetch(self.get_url('/fish'), self.stop)
        response = self.wait()

        self.assertEqual(404, response.code)


if __name__ == '__main__':
    unittest.main()

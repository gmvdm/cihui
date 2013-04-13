# -*- coding: utf-8 -*-
# Copyright (c) 2012 Geoff Wilson <gmwils@gmail.com>

import unittest

from tornado.testing import AsyncHTTPTestCase
from cihui import app


class AccountData:
    pass


class ListData:
    def get_lists(self, callback):
        callback([{'id': 123, 'title': 'list123', 'stub': 'test-stub'}])


class DisplayWordListsTest(AsyncHTTPTestCase):
    def get_app(self):
        self.account_db = AccountData()
        self.list_db = ListData()
        return app.CiHuiApplication(self.account_db, self.list_db)

    def setUp(self):
        AsyncHTTPTestCase.setUp(self)

    def test_show_homepage(self):
        self.http_client.fetch(self.get_url('/'), self.stop)
        response = self.wait()

        self.assertEqual(200, response.code)
        self.assertIn(b'list123', response.body)
        self.assertIn(b'123-test-stub', response.body)

    def test_invalid_url(self):
        self.http_client.fetch(self.get_url('/fish'), self.stop)
        response = self.wait()

        self.assertEqual(404, response.code)


class NoListData:
    def get_lists(self, callback):
        callback(None)


class DisplayNoWordListsTest(AsyncHTTPTestCase):
    def get_app(self):
        self.account_db = AccountData()
        self.list_db = NoListData()
        return app.CiHuiApplication(self.account_db, self.list_db)

    def setUp(self):
        AsyncHTTPTestCase.setUp(self)

    def test_no_word_lists(self):
        self.http_client.fetch(self.get_url('/'), self.stop)
        response = self.wait()

        self.assertEqual(200, response.code)
        self.assertIn(b'CiHui', response.body)


if __name__ == '__main__':
    unittest.main()

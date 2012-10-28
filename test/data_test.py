# -*- coding: utf-8 -*-
# Copyright (c) 2012 Geoff Wilson <gmwils@gmail.com>

import mock
import unittest

from tornado.testing import AsyncHTTPTestCase
from cihui import data


class TestMapDbUrl(unittest.TestCase):
    def test_simple_example(self):
        url = 'postgresql://username:pass@hostname:1234/dbname'
        expectations = {'host': 'hostname',
                        'database': 'dbname',
                        'user': 'username',
                        'password': 'pass'}
        settings = data.build_settings_from_dburl(url)

        for k, v in expectations.items():
            self.assertEqual(settings[k], v)


class GetAccountTest(AsyncHTTPTestCase):
    def get_app(self):
        self.app = mock.Mock()
        return self.app

    def setUp(self):
        AsyncHTTPTestCase.setUp(self)
        self.db = mock.Mock()
        self.database = data.Database('', self.db)
        self.callback = mock.Mock()

    def test_get_account_sql(self):
        self.database.get_account('user@example.com', self.callback)
        self.db.batch.assert_called_once_with(
            {'user@example.com': ['SELECT * FROM user WHERE email = "%s";', ('user@example.com',)]},
            callback=self.database._on_get_account_response)

        self.assertEqual(self.database.callbacks['user@example.com'], self.callback)

    def test_no_account_found(self):
        self.database.callbacks['user@example.com'] = self.callback
        self.database._on_get_account_response({'user@example.com': ''})

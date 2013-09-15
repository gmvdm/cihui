# -*- coding: utf-8 -*-
# Copyright (c) 2012 Geoff Wilson <gmwils@gmail.com>

import mock

from tornado.testing import AsyncHTTPTestCase
from cihui.data import account


class AccountDataTest(AsyncHTTPTestCase):
    def get_app(self):
        self.app = mock.Mock()
        return self.app

    def setUp(self):
        AsyncHTTPTestCase.setUp(self)
        self.db = mock.Mock()
        self.callback = mock.Mock()
        self.accountdata = account.AccountData('', self.db)


class AuthenticateAccountTest(AccountDataTest):
    def test_authenticate_basic_account(self):
        self.assertTrue(
            self.accountdata.authenticate_api_user('user', 'secret'))

    def test_no_authenticate_basic_account(self):
        self.assertFalse(
            self.accountdata.authenticate_api_user('user', 'badpassword'))


class GetAccountTest(AccountDataTest):
    def test_get_account_sql(self):
        self.accountdata.get_account('user@example.com', self.callback)
        self.db.execute.assert_called_once()
        self.assertEqual(self.accountdata.callbacks['0|user@example.com'], self.callback)

    # TODO(gmwils): improve testing for accounts

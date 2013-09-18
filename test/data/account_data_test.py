# -*- coding: utf-8 -*-
# Copyright (c) 2012 Geoff Wilson <gmwils@gmail.com>

import mock
import unittest

from tornado.testing import AsyncHTTPTestCase
from cihui.data import account


class DigestTest(unittest.TestCase):
    def test_identical_digest(self):
        d1 = account.build_password_digest('password', 'salt')
        d2 = account.build_password_digest('password', 'salt')

        self.assertEqual(d1, d2)

    def test_different_salt(self):
        d1 = account.build_password_digest('password', 'salt1')
        d2 = account.build_password_digest('password', 'salt2')

        self.assertNotEqual(d1, d2)

    def test_different_passwd(self):
        d1 = account.build_password_digest('password1', 'salt')
        d2 = account.build_password_digest('password2', 'salt')

        self.assertNotEqual(d1, d2)


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

    def test_auth_web_user(self):
        self.accountdata.authenticate_web_user('user', 'secret', '/next',
                                               self.callback)
        self.db.execute.assert_called_once()
        self.assertEqual(self.accountdata.callbacks['0|user'], self.callback)

    def test_auth_web_user_response_empty(self):
        cursor = mock.MagicMock(side_effects=[])

        self.accountdata.callbacks['0|user'] = self.callback
        self.accountdata._on_authenticate_web_user('secret', '/next', '0|user', cursor)

        self.callback.assert_called_once_with()

    def test_auth_web_user_response_error(self):
        cursor = mock.MagicMock(side_effects=[])

        self.accountdata.callbacks['0|user'] = self.callback
        self.accountdata._on_authenticate_web_user('secret', '/next', '0|user', cursor, 'Error')

        self.callback.assert_called_once_with()

    def test_auth_web_user_response_invalid_password(self):
        cursor = mock.MagicMock(side_effects=[])
        passwd_hash = ''
        passwd_salt = ''
        cursor.rowcount = 1
        cursor.fetchone.return_value = tuple([1, 'test@exmaple.com', passwd_hash, passwd_salt])

        self.accountdata.callbacks['0|user'] = self.callback
        self.accountdata._on_authenticate_web_user('secret', '/next', '0|user', cursor)

        self.callback.assert_called_once_with()

    def test_auth_web_user_response_valid_password(self):
        passwd_salt = 'testsalt'
        passwd_hash = account.build_password_digest('secret', passwd_salt).decode()

        cursor = mock.MagicMock(side_effects=[])
        cursor.rowcount = 1
        cursor.fetchone.return_value = tuple([1, 'test@example.com', passwd_hash, passwd_salt])

        self.accountdata.callbacks['0|user'] = self.callback
        self.accountdata._on_authenticate_web_user('secret', '/next', '0|user', cursor)

        self.callback.assert_called_once_with(1, '/next', 'test@example.com')


class GetAccountTest(AccountDataTest):
    def test_get_account_sql(self):
        self.accountdata.get_account('user@example.com', self.callback)
        self.db.execute.assert_called_once()
        self.assertEqual(self.accountdata.callbacks['0|user@example.com'], self.callback)

    # TODO(gmwils): improve testing for accounts

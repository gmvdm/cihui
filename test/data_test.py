# -*- coding: utf-8 -*-
# Copyright (c) 2012 Geoff Wilson <gmwils@gmail.com>

import mock
import unittest

from tornado.testing import AsyncHTTPTestCase
from cihui import data


class AccountDataTest(AsyncHTTPTestCase):
    def get_app(self):
        self.app = mock.Mock()
        return self.app

    def setUp(self):
        AsyncHTTPTestCase.setUp(self)
        self.db = mock.Mock()
        self.callback = mock.Mock()
        self.accountdata = data.AccountData('', self.db)


class ListDataTest(AsyncHTTPTestCase):
    def get_app(self):
        self.app = mock.Mock()
        return self.app

    def setUp(self):
        AsyncHTTPTestCase.setUp(self)
        self.db = mock.Mock()
        self.callback = mock.Mock()
        self.listdata = data.ListData('', self.db)


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
        self.db.batch.assert_called_once_with(
            {'0|user@example.com': ['SELECT * FROM account WHERE email = %s;', ('user@example.com',)]},
            callback=self.accountdata._on_get_account_response)

        self.assertEqual(self.accountdata.callbacks['0|user@example.com'], self.callback)

    def test_no_account_found(self):
        self.accountdata.callbacks['0|user@example.com'] = self.callback
        self.accountdata._on_get_account_response({'0|user@example.com': ''})


class GetManyListsTest(ListDataTest):
    def test_get_lists_sql(self):
        self.listdata.get_lists(self.callback)
        self.db.batch.assert_called_once()
        self.assertEqual(self.listdata.callbacks['0|'], self.callback)

    def test_got_lists(self):
        cursor = mock.MagicMock(side_effect=[])

        self.listdata.callbacks['0|'] = self.callback
        self.listdata._on_get_lists_response({'0|': cursor})

        self.callback.assert_called_once_with([])


class GetWordListTest(ListDataTest):
    def test_get_basic_list(self):
        self.listdata.get_word_list(12, self.callback)
        self.db.batch.assert_called_once()
        self.assertEqual(self.listdata.callbacks['0|12'], self.callback)

    def test_got_no_word_list(self):
        cursor = mock.MagicMock(side_effect=[])

        self.listdata.callbacks['0|'] = self.callback
        self.listdata._on_get_word_list_response({'0|': cursor})

        self.callback.assert_called_once_with(None)

    def test_got_one_word_list_with_no_words(self):
        cursor = mock.MagicMock(side_effect=[])
        cursor.rowcount = 1
        cursor.fetchone.return_value = tuple([1, 'Test', None])

        self.listdata.callbacks['0|1'] = self.callback
        self.listdata._on_get_word_list_response({'0|1': cursor})

        self.callback.assert_called_once_with({'id': 1,
                                               'title': 'Test',
                                               'words': None})

    def test_got_one_word_list_with_words(self):
        cursor = mock.MagicMock(side_effect=[])
        cursor.rowcount = 1
        cursor.fetchone.return_value = tuple([1, 'Test', '{"key": "value"}'])

        self.listdata.callbacks['0|1'] = self.callback
        self.listdata._on_get_word_list_response({'0|1': cursor})

        self.callback.assert_called_once_with({'id': 1,
                                               'title': 'Test',
                                               'words': {'key': 'value'}})


class CreateListTest(ListDataTest):
    def test_create_empty_list_sql(self):
        self.listdata.create_list('Test List', [], self.callback)
        self.db.batch.assert_called_once()
        self.assertIn('INSERT', str(self.db.batch.call_args))
        self.assertIn('test-list', str(self.db.batch.call_args))
        self.assertEqual(self.listdata.callbacks['0|Test List'], self.callback)

    def test_create_word_list_sql(self):
        self.listdata.create_list('Word List', [['大', 'da', ['big']], ], self.callback)
        self.db.batch.assert_called_once()
        self.assertIn('INSERT', str(self.db.batch.call_args))
        self.assertEqual(self.listdata.callbacks['0|Word List'], self.callback)

    def test_update_existing_list(self):
        self.listdata.create_list('Test List', [], self.callback, True)
        self.db.batch.assert_called_once()
        self.assertIn('UPDATE', str(self.db.batch.call_args))
        self.assertIn('test-list', str(self.db.batch.call_args))
        self.assertEqual(self.listdata.callbacks['0|Test List'], self.callback)

    def test_created_list(self):
        cursor = mock.Mock()

        self.listdata.callbacks['0|testlist'] = self.callback
        self.listdata._on_create_list_response({'0|testlist': cursor})

        self.callback.assert_called_once_with(True)

    def test_callback_failed_and_second_succeeded(self):
        cursor = mock.Mock()

        self.listdata.callbacks['0|testlist'] = self.callback
        self.listdata._on_create_list_response({'1|false list': cursor,
                                                '0|testlist': cursor})

        self.callback.assert_called_once_with(True)


class ListExistsTest(ListDataTest):
    def test_list_exists(self):
        self.listdata.list_exists('list name', self.callback)
        self.db.batch.assert_called_once()
        self.assertEqual(self.listdata.callbacks['0|list name'], self.callback)

    def test_on_list_exists(self):
        cursor = mock.MagicMock(side_effect=[])
        cursor.fetchone.return_value = tuple([1])

        self.listdata.callbacks['0|testlist'] = self.callback
        self.listdata._on_list_exists({'0|testlist': cursor})

        self.callback.assert_called_once_with(True)

    def test_on_list_not_exists(self):
        cursor = mock.MagicMock(side_effect=[])
        cursor.fetchone.return_value = tuple([0])

        self.listdata.callbacks['0|testlist'] = self.callback
        self.listdata._on_list_exists({'0|testlist': cursor})

        self.callback.assert_called_once_with(False)

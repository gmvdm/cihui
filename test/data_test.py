# -*- coding: utf-8 -*-
# Copyright (c) 2012 Geoff Wilson <gmwils@gmail.com>

import mock
import unittest

from tornado.testing import AsyncHTTPTestCase
from cihui import data


class BaseDataTest(AsyncHTTPTestCase):
    def get_app(self):
        self.app = mock.Mock()
        return self.app

    def setUp(self):
        AsyncHTTPTestCase.setUp(self)
        self.db = mock.Mock()
        self.database = data.Database('', self.db)
        self.callback = mock.Mock()


class GetAccountTest(BaseDataTest):
    def test_get_account_sql(self):
        self.database.get_account('user@example.com', self.callback)
        self.db.batch.assert_called_once_with(
            {'0|user@example.com': ['SELECT * FROM account WHERE email = %s;', ('user@example.com',)]},
            callback=self.database._on_get_account_response)

        self.assertEqual(self.database.callbacks['0|user@example.com'], self.callback)

    def test_no_account_found(self):
        self.database.callbacks['0|user@example.com'] = self.callback
        self.database._on_get_account_response({'0|user@example.com': ''})


class GetManyListsTest(BaseDataTest):
    def test_get_lists_sql(self):
        self.database.get_lists(self.callback)
        self.db.batch.assert_called_once()
        self.assertEqual(self.database.callbacks['0|'], self.callback)

    def test_got_lists(self):
        cursor = mock.MagicMock(side_effect=[])

        self.database.callbacks['0|'] = self.callback
        self.database._on_get_lists_response({'0|': cursor})

        self.callback.assert_called_once_with([])


class GetWordListTest(BaseDataTest):
    def test_get_basic_list(self):
        self.database.get_word_list(12, self.callback)
        self.db.batch.assert_called_once()
        self.assertEqual(self.database.callbacks['0|12'], self.callback)


class CreateListTest(BaseDataTest):
    def test_create_empty_list_sql(self):
        self.database.create_list('Test List', [], self.callback)
        self.db.batch.assert_called_once()
        self.assertIn('INSERT', str(self.db.batch.call_args))
        self.assertEqual(self.database.callbacks['0|Test List'], self.callback)

    def test_create_word_list_sql(self):
        self.database.create_list('Word List', [[u'大', 'da', ['big']], ], self.callback)
        self.db.batch.assert_called_once()
        self.assertIn('INSERT', str(self.db.batch.call_args))
        self.assertEqual(self.database.callbacks['0|Word List'], self.callback)

    def test_update_existing_list(self):
        self.database.create_list('Test List', [], self.callback, True)
        self.db.batch.assert_called_once()
        self.assertIn('UPDATE', str(self.db.batch.call_args))
        self.assertEqual(self.database.callbacks['0|Test List'], self.callback)

    def test_created_list(self):
        cursor = mock.Mock()

        self.database.callbacks['0|testlist'] = self.callback
        self.database._on_create_list_response({'0|testlist': cursor})

        self.callback.assert_called_once_with(True)

    def test_callback_failed_and_second_succeeded(self):
        cursor = mock.Mock()

        self.database.callbacks['0|testlist'] = self.callback
        self.database._on_create_list_response({'1|false list': cursor,
                                                '0|testlist': cursor})

        self.callback.assert_called_once_with(True)


class ListExistsTest(BaseDataTest):
    def test_list_exists(self):
        self.database.list_exists('list name', self.callback)
        self.db.batch.assert_called_once()
        self.assertEqual(self.database.callbacks['0|list name'], self.callback)

    def test_on_list_exists(self):
        cursor = mock.MagicMock(side_effect=[])
        cursor.fetchone.return_value = tuple([1])

        self.database.callbacks['0|testlist'] = self.callback
        self.database._on_list_exists({'0|testlist': cursor})

        self.callback.assert_called_once_with(True)

    def test_on_list_not_exists(self):
        cursor = mock.MagicMock(side_effect=[])
        cursor.fetchone.return_value = tuple([0])

        self.database.callbacks['0|testlist'] = self.callback
        self.database._on_list_exists({'0|testlist': cursor})

        self.callback.assert_called_once_with(False)

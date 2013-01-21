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
            {'user@example.com': ['SELECT * FROM account WHERE email = %s;', ('user@example.com',)]},
            callback=self.database._on_get_account_response)

        self.assertEqual(self.database.callbacks['user@example.com'], self.callback)

    def test_no_account_found(self):
        self.database.callbacks['user@example.com'] = self.callback
        self.database._on_get_account_response({'user@example.com': ''})


class GetManyListsTest(BaseDataTest):
    def test_get_lists_sql(self):
        self.database.get_lists(self.callback)
        self.db.batch.assert_called_once()
        self.assertEqual(self.database.list_callbacks[0], self.callback)

    def test_got_lists(self):
        cursor = mock.MagicMock(side_effect=[])

        self.database.list_callbacks[0] = self.callback
        self.database._on_get_lists_response({0: cursor})

        self.callback.assert_called_once_with([])


class CreateListTest(BaseDataTest):
    def test_create_empty_list_sql(self):
        self.database.create_list('Test List', [], self.callback)
        self.db.batch.assert_called_once()
        self.assertEqual(self.database.create_list_callbacks['Test List'], self.callback)

        # TODO(gmwils) actually test SQL called with right values

    def test_created_list(self):
        cursor = mock.Mock()

        self.database.create_list_callbacks['testlist'] = self.callback
        self.database._on_create_list_response({'testlist': cursor})

        self.callback.assert_called_once_with(True)

    def test_callback_failed_and_second_succeeded(self):
        cursor = mock.Mock()

        self.database.create_list_callbacks['testlist'] = self.callback
        self.database._on_create_list_response({'false list': cursor,
                                                'testlist': cursor})

        self.callback.assert_called_once_with(True)

    def test_create_word_list_sql(self):
        self.database.create_list('Word List', [], self.callback)
        self.db.batch.assert_called_once()
        self.assertEqual(self.database.create_list_callbacks['Word List'], self.callback)

        # TODO(gmwils) actually test SQL

    # TODO(gmwils) handle duplicates
    def test_create_duplicate_list(self):
        pass
        self.database.create_list('Word List', [], self.callback)
        self.db.batch.assert_called_once()  # INSERT
        self.database.create_list('Word List', [[u'大', 'da', ['big']], ], self.callback)
        self.db.batch.assert_called_once()  # UPDATE

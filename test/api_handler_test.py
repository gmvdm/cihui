# -*- coding: utf-8 -*-
# Copyright (c) 2012 Geoff Wilson <gmwils@gmail.com>

import json
import mock
import unittest
import urllib

import support
from cihui import api_handler

from tornado.testing import AsyncHTTPTestCase


# TODO(gmwils): add tests for authentication for the API
class APITestBase(support.HandlerTestCase):
    def setUp(self):
        self.account_data_layer = mock.Mock()
        self.list_data_layer = mock.Mock()

        AsyncHTTPTestCase.setUp(self)

    def url_encode_data(self, data):
        self.data = urllib.urlencode(data)
        return self.data

    def json_encode_data(self, data):
        self.data = json.dumps(data)
        return self.data


class AccountTest(APITestBase):
    def get_handlers(self):
        class Data:
            def get_account(self, email, callback):
                callback({'email': email, 'id': 'id123'})

            def authenticate_api_user(self, user, passwd):
                return True

        self.account_data_layer = Data()
        return [(r'/api/account', api_handler.APIAccountHandler, dict(account_db=self.account_data_layer))]

    def test_find_or_create_account(self):
        data = self.url_encode_data({'email': 'test@example.com'})

        self.http_client.fetch(self.get_url('/api/account'), self.stop, method='POST',
                               headers=None, body=data,
                               auth_username='user', auth_password='secret')
        response = self.wait()

        self.assertEqual(200, response.code)
        self.assertIn('test@example.com', response.body)
        self.assertIn('id123', response.body)

    def test_create_account(self):
        pass


class ListTest(APITestBase):
    def get_handlers(self):
        class AccountData:
            def authenticate_api_user(self, user, passwd):
                return True

        class ListData:
            def create_list(self, list_name, words, callback, exists=False):
                callback(True)

            def list_exists(self, list_name, callback):
                callback(True)

        self.account_data_layer = AccountData()
        self.list_data_layer = ListData()

        return [(r'/api/list',
                 api_handler.APIListHandler,
                 dict(account_db=self.account_data_layer,
                      list_db=self.list_data_layer))]

    def test_create_list(self):
        data = self.json_encode_data({'title': 'Test List',
                                      'words': [[u'大', 'da', 'big'], ]
                                      })

        self.http_client.fetch(self.get_url('/api/list'), self.stop, method='POST',
                               headers=None, body=data,
                               auth_username='user', auth_password='secret')
        response = self.wait()

        self.assertEqual(201, response.code)

    def test_update_existing_list(self):
        # TODO(gmwils): fill in the test
        pass

    def test_fail_on_create_empty_list(self):
        data = self.json_encode_data({'title': 'Test List', 'words': ''})
        self.http_client.fetch(self.get_url('/api/list'), self.stop, method='POST',
                               headers=None, body=data,
                               auth_username='user', auth_password='secret')
        response = self.wait()

        self.assertEqual(500, response.code)
        self.assertIn('No word list', response.body)

    def test_fail_on_missing_list(self):
        data = self.json_encode_data({'title': 'Test List'})
        self.http_client.fetch(self.get_url('/api/list'), self.stop, method='POST',
                               headers=None, body=data,
                               auth_username='user', auth_password='secret')
        response = self.wait()

        self.assertEqual(500, response.code)

    def test_fail_on_missing_title(self):
        data = self.json_encode_data({})
        self.http_client.fetch(self.get_url('/api/list'), self.stop, method='POST',
                               headers=None, body=data,
                               auth_username='user', auth_password='secret')
        response = self.wait()

        self.assertEqual(500, response.code)
        self.assertIn('Missing title', response.body)

# -*- coding: utf-8 -*-
# Copyright (c) 2012 Geoff Wilson <gmwils@gmail.com>

import json
import support
import urllib.error
import urllib.parse
import urllib.request

from cihui import api_handler
from tornado.testing import AsyncHTTPTestCase


class APITestBase(support.HandlerTestCase):
    def setUp(self):
        AsyncHTTPTestCase.setUp(self)

    def url_encode_data(self, data):
        self.data = urllib.parse.urlencode(data)
        return self.data

    def json_encode_data(self, data):
        self.data = json.dumps(data)
        return self.data


class AuthTest(APITestBase):
    def get_handlers(self):
        class Data:
            def authenticate_api_user(self, user, passwd):
                return (user == 'user' and passwd == 'secret')

        self.data_layer = Data()

        class MainHandler(api_handler.APIHandler):
            def get(self):
                self.write("Hello, world")

        return [(r'/api', MainHandler, dict(account_db=self.data_layer))]

    def test_successful_authentication(self):
        self.http_client.fetch(self.get_url('/api'), self.stop, method='GET',
                               headers=None, body=None,
                               auth_username='user', auth_password='secret')
        response = self.wait()

        self.assertEqual(200, response.code)
        self.assertIn(b'Hello', response.body)

    def test_failed_authentication(self):
        self.http_client.fetch(self.get_url('/api'), self.stop, method='GET',
                               headers=None, body=None,
                               auth_username='baduser', auth_password='notsecret')
        response = self.wait()

        self.assertEqual(401, response.code)
        self.assertNotIn(b'Hello', response.body)

    def test_no_authentication(self):
        self.http_client.fetch(self.get_url('/api'), self.stop)
        response = self.wait()

        self.assertEqual(401, response.code)
        self.assertNotIn(b'Hello', response.body)


class AccountTest(APITestBase):
    def get_handlers(self):
        class Data:
            def get_account(self, email, callback):
                callback({'email': email, 'id': 'id123'})

            def authenticate_api_user(self, user, passwd):
                return True

        self.account_data_layer = Data()
        return [(r'/api/account',
                 api_handler.APIAccountHandler,
                 dict(account_db=self.account_data_layer))]

    def test_find_or_create_account(self):
        data = self.url_encode_data({'email': 'test@example.com'})

        self.http_client.fetch(self.get_url('/api/account'), self.stop, method='POST',
                               headers=None, body=data,
                               auth_username='user', auth_password='secret')
        response = self.wait()

        self.assertEqual(200, response.code)
        self.assertIn(b'test@example.com', response.body)
        self.assertIn(b'id123', response.body)

    def test_create_account(self):
        pass


class ListTest(APITestBase):
    def get_handlers(self):
        class AccountData:
            def authenticate_api_user(self, user, passwd):
                return True

        class ListData:
            def create_list(self, list_name, words, callback, exists=False, account_id=None, email_address=None):
                self.words = words
                self.account_id = account_id
                self.email_address = email_address
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
                                      'words': [['很', 'he\u0301n', ['very']], ],
                                      'account_id': 1,
                                      })

        self.http_client.fetch(self.get_url('/api/list'), self.stop, method='POST',
                               headers=None, body=data,
                               auth_username='user', auth_password='secret')
        response = self.wait()

        self.assertEqual(201, response.code)
        self.assertIn('很', self.list_data_layer.words[0])
        self.assertEqual('hén', self.list_data_layer.words[0][1])
        self.assertEqual(self.list_data_layer.account_id, 1)

    def test_create_list_requires_user(self):
        data = self.json_encode_data({'title': 'Test List',
                                      'words': [['很', 'he\u0301n', ['very']], ],
                                      })

        self.http_client.fetch(self.get_url('/api/list'), self.stop, method='POST',
                               headers=None, body=data,
                               auth_username='user', auth_password='secret')
        response = self.wait()

        self.assertEqual(500, response.code)

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
        self.assertIn(b'No word list', response.body)

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
        self.assertIn(b'Missing title', response.body)

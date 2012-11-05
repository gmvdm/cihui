# -*- coding: utf-8 -*-
# Copyright (c) 2012 Geoff Wilson <gmwils@gmail.com>

import mock
import unittest
import urllib

from tornado.testing import AsyncHTTPTestCase
from cihui import app


# TODO(gmwils): add authentication for the API
class APITestBase(AsyncHTTPTestCase):
    def get_app(self):
        self.data_layer = mock.Mock()
        return app.CiHuiApplication(self.data_layer)

    def setUp(self):
        AsyncHTTPTestCase.setUp(self)

    # TODO(gmwils): this should be JSON
    def build_data(self, data):
        self.data = urllib.urlencode(data)
        return self.data


class AccountTest(APITestBase):
    def get_app(self):
        class Data:
            def get_account(self, email, callback):
                callback({'email': email, 'id': 'id123'})

        self.data_layer = Data()
        return app.CiHuiApplication(self.data_layer)

    def test_find_or_create_account(self):
        data = self.build_data({'email': 'test@example.com'})

        self.http_client.fetch(self.get_url('/api/account'), self.stop, method='POST',
                               headers=None, body=data)
        response = self.wait()

        self.assertEqual(200, response.code)
        self.assertIn('test@example.com', response.body)
        self.assertIn('id123', response.body)

    def test_create_account(self):
        pass


class ListTest(APITestBase):
    def get_app(self):
        class Data:
            def create_list(self, list_name, words, callback):
                callback({'name': list_name, 'id': 'list123', 'words': words})

        self.data_layer = Data()
        return app.CiHuiApplication(self.data_layer)

    def test_create_list(self):
        data = self.build_data({'list': 'Test List',
                                'words': [(u'大', 'da', 'big'), ]})

        self.http_client.fetch(self.get_url('/api/list'), self.stop, method='POST',
                               headers=None, body=data)
        response = self.wait()

        self.assertIn('Test List', response.body)
        self.assertIn('list123', response.body)
        # TODO(gmwils): sort out encoding of data
        # self.assertIn(u'大', response.body)

    def test_update_existing_list(self):
        pass

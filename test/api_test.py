# -*- coding: utf-8 -*-
# Copyright (c) 2012 Geoff Wilson <gmwils@gmail.com>

import mock
import unittest
import urllib

from tornado.testing import AsyncHTTPTestCase
from cihui import app

def build_data(data):
    return urllib.urlencode(data)

class APITest(AsyncHTTPTestCase):

    def get_app(self):
        self.data_layer = mock.Mock()
        return app.CiHuiApplication(self.data_layer)

    def setUp(self):
        AsyncHTTPTestCase.setUp(self)


    def test_post_new_list(self):
        data = build_data({'email': 'test@example.com',
                           'list': 'Test List',
                           'words': '...'})
        self.data_layer.get_account.return_value = 'id123'

        self.http_client.fetch(self.get_url('/api/word'), self.stop, method='POST',
                               headers=None, body=data)
        response = self.wait()

        self.assertEqual(200, response.code)
        self.assertIn('test@example.com', response.body)
        self.assertIn('id123', response.body)

        self.data_layer.get_account.assert_called_once_with('test@example.com')

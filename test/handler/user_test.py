# -*- coding: utf-8 -*-
# Copyright (c) 2012 Geoff Wilson <gmwils@gmail.com>

import urllib.parse

from cihui.handler import user
from cihui import support


class UserTest(support.UITestCase):
    def setUp(self):
        class AccountData:
            def create_account(self, user, password, callback):
                if password == 'bad':
                    callback(None)
                else:
                    callback(123)

            def get_account_by_id(self, user_id, callback):
                callback({'account_name': 'Tester'})

        self.account_db = AccountData()
        super(UserTest, self).setUp()

    def get_handlers(self):
        return [(r'/user/(\w+)$', user.UserHandler,
                 dict(account_db=self.account_db)),
                (r'/user/(\w+)/(\w+)$', user.UserHandler,
                 dict(account_db=self.account_db)),
                (r'/user', user.UserHandler,
                 dict(account_db=self.account_db))]

    def test_show_new_user_page(self):
        self.http_client.fetch(self.get_url('/user/new'), self.stop)
        response = self.wait()

        self.assertEqual(200, response.code)
        self.assertIn(b'Create a new account', response.body)

    def test_show_specific_user(self):
        self.http_client.fetch(self.get_url('/user/test_user'), self.stop)
        response = self.wait()

        self.assertEqual(200, response.code)
        self.assertIn(b'test_user', response.body)
        self.assertIn(b'Tester', response.body)

    def test_show_user_edit(self):
        self.http_client.fetch(self.get_url('/user/test_user/edit'), self.stop)
        response = self.wait()

        self.assertEqual(200, response.code)
        self.assertIn(b'test_user', response.body)
        self.assertIn(b'Tester', response.body)

    def test_create_account(self):
        params = {'email': 'john@example.com', 'password': 'good'}
        body = urllib.parse.urlencode(params)
        self.http_client.fetch(self.get_url('/user'), self.stop,
                               method='POST',
                               headers=None,
                               body=body,
                               follow_redirects=False)
        response = self.wait()

        self.assertEqual(302, response.code)
        self.assertEqual('/user/123', response.headers['Location'])

    def test_fail_create_account(self):
        params = {'email': 'john@example.com', 'password': 'bad'}
        body = urllib.parse.urlencode(params)
        self.http_client.fetch(self.get_url('/user'), self.stop,
                               method='POST',
                               headers=None,
                               body=body,
                               follow_redirects=False)
        response = self.wait()

        self.assertEqual(302, response.code)
        self.assertEqual('/', response.headers['Location'])

    # TODO(gmwils): add test cases for invalid arguements (bad formatting, insecure, etc)

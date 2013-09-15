# -*- coding: utf-8 -*-
# Copyright (c) 2012 Geoff Wilson <gmwils@gmail.com>

import tornado
import urllib.parse

from cihui.handler import auth
from cihui import support


class LoginTest(support.UITestCase):
    def setUp(self):
        class AccountData:
            def authenticate_web_user(self, user, password, next_url, cb):
                account_id = 123

                if password == 'bad':
                    cb()
                else:
                    cb(account_id, next_url, 'test_username')

        self.account_db = AccountData()
        super(LoginTest, self).setUp()

    def get_handlers(self):
        class HomeHandler(tornado.web.RequestHandler):
            def get(self):
                self.write(self.request.uri)

        return [(r'/login',
                 auth.LoginHandler,
                 dict(account_db=self.account_db)),
                (r'/logout', auth.LogoutHandler),
                (r'/.*', HomeHandler)]

    def test_show_login(self):
        self.http_client.fetch(self.get_url('/login'), self.stop)
        response = self.wait()
        self.assertEqual(200, response.code)
        # TODO(gmwils): Improve test of render of login form
        self.assertIn(b'login', response.body)

    def test_successful_login(self):
        params = {'user': 'john', 'password': 'secret', 'next': '/example'}
        body = urllib.parse.urlencode(params)
        self.http_client.fetch(self.get_url('/login'), self.stop,
                               method='POST',
                               headers=None,
                               body=body,
                               follow_redirects=False)
        response = self.wait()

        self.assertEqual(302, response.code)
        self.assertIn('session_id=', response.headers['Set-Cookie'])
        self.assertEqual('/example', response.headers['Location'])

    def test_failed_login(self):
        params = {'user': 'john', 'password': 'bad', 'next': '/example'}
        body = urllib.parse.urlencode(params)
        self.http_client.fetch(self.get_url('/login'), self.stop,
                               method='POST',
                               headers=None,
                               body=body,
                               follow_redirects=False)
        response = self.wait()

        self.assertEqual(302, response.code)
        self.assertEqual('/login?error=Error%3A+Incorrect+login', response.headers['Location'])

    def test_logout(self):
        self.http_client.fetch(self.get_url('/logout'), self.stop, follow_redirects=False)
        response = self.wait()

        self.assertIn('session_id=', response.headers['Set-Cookie'])

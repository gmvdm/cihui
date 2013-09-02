# -*- coding: utf-8 -*-
# Copyright (c) 2012 Geoff Wilson <gmwils@gmail.com>

import mock
import os
import support
import tornado
import unittest
import urllib.parse

from cihui import handler

from tornado.testing import AsyncHTTPTestCase


class UITestCase(support.HandlerTestCase):
    def get_app_kwargs(self):
        args = super().get_app_kwargs()
        args['static_path'] = os.path.join(os.path.dirname(__file__), '../static')
        args['template_path'] = os.path.join(os.path.dirname(__file__), '../templates')
        return args


class LoginTest(UITestCase):
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
                 handler.LoginHandler,
                 dict(account_db=self.account_db)),
                (r'/logout', handler.LogoutHandler),
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
        self.assertEqual('/', response.headers['Location'])

    def test_logout(self):
        self.http_client.fetch(self.get_url('/logout'), self.stop, follow_redirects=False)
        response = self.wait()

        self.assertIn('session_id=', response.headers['Set-Cookie'])



class UserTest(UITestCase):
    def setUp(self):
        class AccountData:
            def create_account(self, user, password, callback):
                if password == 'bad':
                    callback(None)
                else:
                    callback(123)

        self.account_db = AccountData()
        super(UserTest, self).setUp()

    def get_handlers(self):
        return [(r'/user/(\w+)$', handler.UserHandler,
                 dict(account_db=self.account_db)),
                (r'/user', handler.UserHandler,
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


class AtomFeedTest(support.HandlerTestCase):
    def setUp(self):
        class ListData:
            def get_lists(self, callback):
                callback([{'title': 'Test Item'}])
        self.list_db = ListData()
        super(AtomFeedTest, self).setUp()

    def get_handlers(self):
        return [(r'/atom.xml',
                 handler.AtomHandler,
                 dict(list_db=self.list_db))]

    def test_atom_feed(self):
        self.http_client.fetch(self.get_url('/atom.xml'), self.stop)
        response = self.wait()

        self.assertEqual(200, response.code)
        self.assertIn(b'Test Item', response.body)


class DisplayWordListTest(UITestCase):
    def setUp(self):
        class ListData:
            def get_word_list(self, list_id, callback):
                if list_id not in [404]:
                    words = [['大', 'da', ['big']], ]
                    callback({'id': list_id,
                              'title': 'list_%d' % list_id,
                              'words': words,
                              'modified_at': mock.Mock()})
                else:
                    callback(None)

        self.list_db = ListData()

        AsyncHTTPTestCase.setUp(self)

    def get_handlers(self):
        return [(r'/list/([0-9]+)[^\.]*(\.?\w*)',
                 handler.WordListHandler,
                 dict(list_db=self.list_db))]

    def test_show_word_list(self):
        self.http_client.fetch(self.get_url('/list/123'), self.stop)
        response = self.wait()

        self.assertEqual(200, response.code)
        self.assertIn(b'list_123', response.body)

    def test_missing_list(self):
        self.http_client.fetch(self.get_url('/list/404'), self.stop)
        response = self.wait()

        self.assertEqual(404, response.code)

    def test_descriptive_stub(self):
        self.http_client.fetch(self.get_url('/list/101-some-great-list'), self.stop)
        response = self.wait()

        self.assertEqual(200, response.code)

    def test_csv_output(self):
        self.http_client.fetch(self.get_url('/list/102.csv'), self.stop)
        response = self.wait()

        self.assertEqual(200, response.code)
        self.assertIn('text/csv', response.headers['Content-Type'])
        self.assertIn(b'big', response.body)


if __name__ == '__main__':
    unittest.main()

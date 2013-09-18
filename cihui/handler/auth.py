# -*- coding: utf-8 -*-
# Copyright (c) 2012 Geoff Wilson <gmwils@gmail.com>

import tornado.web
from cihui.handler import common


class LoginHandler(common.BaseHandler):
    def initialize(self, account_db):
        self.account_db = account_db

    def get(self):
        error_msg = self.get_argument('error', default='')
        self.render('login.html', error_msg=error_msg)

    @tornado.web.asynchronous
    def post(self):
        # TODO(gmwils): document API
        # TODO(gmwils): test from the view layer using selenium
        # TODO(gmwils): require HTTPS for login/app
        username = self.get_argument('user')
        password = self.get_argument('password')
        next_url = self.get_argument('next', '/home')
        self.account_db.authenticate_web_user(username, password, next_url,
                                              self.authenticated)

    @tornado.web.asynchronous
    def authenticated(self, user_id=None, redirect_url=None, username=None):
        if user_id is not None:
            self.set_secure_cookie('session_id', '%s|%s' % (user_id, username),
                                   expires_days=30)
            self.redirect(redirect_url or '/')
        else:
            self.set_secure_cookie('session_id', '')
            error_msg = tornado.escape.url_escape('Error: Incorrect login')
            self.redirect('/login?error=%s' % error_msg)


class LogoutHandler(common.BaseHandler):
    def get(self):
        self.set_secure_cookie('session_id', '')
        self.redirect('/')

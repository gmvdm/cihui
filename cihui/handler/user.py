# -*- coding: utf-8 -*-
# Copyright (c) 2012 Geoff Wilson <gmwils@gmail.com>

import tornado.web

from cihui.handler import common
from tornado import gen


class UserHandler(common.BaseHandler):
    def initialize(self, account_db):
        self.account_db = account_db

    def get(self, username):
        error_msg = self.get_argument('error', default='')
        if username == 'new':
            self.render('user/new.html', error_msg=error_msg)
        else:
            # TODO(gmwils): get user info from the database
            self.render('user/show.html',
                        username=username,
                        error_msg=error_msg)

    @tornado.web.asynchronous
    @gen.engine
    def post(self):
        email = self.get_argument('email')
        passwd = self.get_argument('password')

        # TODO(gmwils): validate the fields
        user_id = yield gen.Task(self.account_db.create_account, email, passwd)

        if user_id is not None:
            self.redirect('/user/%s' % user_id)
        else:
            self.redirect('/')

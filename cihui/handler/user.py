# -*- coding: utf-8 -*-
# Copyright (c) 2012 Geoff Wilson <gmwils@gmail.com>

import tornado.web

from cihui.handler import common
from tornado import gen


class UserHandler(common.BaseHandler):
    def initialize(self, account_db):
        self.account_db = account_db

    @tornado.web.asynchronous
    @gen.engine
    def get(self, user_id):
        error_msg = self.get_argument('error', default='')
        if user_id == 'new':
            self.render('user/new.html', error_msg=error_msg)
            return

        user_info = yield gen.Task(self.account_db.get_account_by_id, user_id)
        user_name = user_info.get('account_name')
        if user_name is None:
            user_name = user_id

        self.render('user/show.html',
                    user_name=user_name,
                    user_id=user_id,
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

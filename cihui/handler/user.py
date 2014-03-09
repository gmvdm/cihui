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
    def get(self, user_id, action=None):
        error_msg = self.get_argument('error', default='')
        if user_id == 'new':
            self.render('user/new.html', error_msg=error_msg)
            return

        user_info = yield gen.Task(self.account_db.get_account_by_id, user_id)
        user_name = user_info.get('account_name')
        user_email = user_info.get('account_email')
        skritter_user = user_info.get('skritter_user', None)

        if user_name is None:
            user_name = user_id

        template_path = 'user/show.html'
        if action == 'edit':
            template_path = 'user/edit.html'

        self.render(template_path,
                    user_name=user_name,
                    user_email=user_email,
                    user_id=user_id,
                    skritter_user=skritter_user,
                    error_msg=error_msg)

    @tornado.web.asynchronous
    @gen.engine
    def post(self, user_id=None):
        # TODO(gmwils): validate the fields
        email = self.get_argument('email')
        passwd = self.get_argument('password')
        username = self.get_argument('username', default=user_id)

        if user_id is None:
            # New account
            new_user_id = yield gen.Task(self.account_db.create_account, email, passwd)

            if new_user_id is not None:
                self.redirect('/user/%s' % new_user_id)
            else:
                self.redirect('/')
        else:
            # Update existing account
            error_msg = yield gen.Task(self.account_db.update_account,
                                       user_id,
                                       email,
                                       username,
                                       passwd)

            if error_msg is None:
                self.redirect('/user/%s' % user_id)
            else:
                self.redirect('/user/%s/edit?error=%s' % (user_id, error_msg))

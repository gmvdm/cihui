# -*- coding: utf-8 -*-
# Copyright (c) 2012 Geoff Wilson <gmwils@gmail.com>

import tornado.web


class MainHandler(tornado.web.RequestHandler):
    def initialize(self, database):
        self.db = database

    @tornado.web.asynchronous
    def get(self):

        self.db.get_lists(self.received_lists)

    def received_lists(self, data):
        msg = u"你好，世界!"

        self.render('index.html', message=msg, data=str(data))
        # self.finish()


class APIWordHandler(tornado.web.RequestHandler):
    def initialize(self, database):
        self.db = database

    def check_xsrf_cookie(self):
        """ Disable cross site cookies on the API methods """
        # TODO(gmwils) determine authentication method for API methods
        pass

    def post(self):
        email = self.get_argument('email', 'No data received')

        account_id = self.db.get_account(email)
        self.write('Received email: "%s", new id: %s' % (email, account_id))

# -*- coding: utf-8 -*-
# Copyright (c) 2012 Geoff Wilson <gmwils@gmail.com>

import tornado.web

class BaseHandler(tornado.web.RequestHandler):
    def initialize(self, database):
        self.db = database

class MainHandler(BaseHandler):
    @tornado.web.asynchronous
    def get(self):
        self.db.get_lists(self.received_lists)

    def received_lists(self, word_lists):
        msg = u"你好，世界!"

        self.render('index.html', message=msg, word_lists=word_lists)


class WordListHandler(BaseHandler):
    @tornado.web.asynchronous
    def get(self, list_id):
        self.db.get_word_list(int(list_id), self.received_list)

    @tornado.web.asynchronous
    def received_list(self, word_list):
        if word_list is not None:
            if word_list.get('words') is None:
                word_list['words'] = []
            self.render('word_list.html', word_list=word_list)
        else:
            self.send_error(404)


class APIHandler(BaseHandler):
    def check_xsrf_cookie(self):
        """ Disable cross site cookies on the API methods """
        # TODO(gmwils) determine authentication method for API methods
        pass


class APIAccountHandler(APIHandler):
    @tornado.web.asynchronous
    def get(self):
        email = self.get_argument('email', None)

        if email is not None:
            self.db.get_account(email, self.got_account)
        else:
            self.got_account(None)

    @tornado.web.asynchronous
    def post(self):
        email = self.get_argument('email', 'No data received')

        self.db.get_account(email, self.got_account)

    def got_account(self, account):
        if account is not None:
            self.write('Received email: "%s", id: %s' % (account['email'], account['id']))
        else:
            # TODO(gmwils): set an error code
            self.write('No account received')

        self.finish()


class APIListHandler(APIHandler):
    @tornado.web.asynchronous
    def post(self):
        list_name = self.get_argument('list', None)
        words = self.get_argument('words', None)

        if list_name is None:
            self.created_list(False, 'Missing title')
            return

        if words is None:
            self.created_list(False, 'No word list supplied')
            return

        self.db.create_list(list_name, words, self.created_list)

    def created_list(self, success, reason=None):
        if success:
            self.write('')
        else:
            self.set_status(500)
            if reason is not None:
                self.write('Error: %s' % reason)
            else:
                self.write('Failed to create list.')

        self.finish()

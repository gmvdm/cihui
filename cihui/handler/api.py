# -*- coding: utf-8 -*-
# Copyright (c) 2012 Geoff Wilson <gmwils@gmail.com>

import base64
import functools
import json
import tornado.web
import unicodedata

from cihui.handler import common


class APIHandler(common.BaseHandler):
    def initialize(self, account_db):
        self.account_db = account_db

    def check_xsrf_cookie(self):
        """ Disable cross site cookies on the API methods """
        pass

    def _execute(self, transforms, *args, **kwargs):
        """ Wrap the _execute method with basic authentication """
        if not self.require_basic_auth(kwargs):
            return False
        return super(APIHandler, self)._execute(transforms, *args, **kwargs)

    def set_unauthorized_headers(self):
        self.set_status(401)
        self.set_header('WWW-Authenticate', 'Basic realm=Restricted')
        self._transforms = []
        self.finish()

    def require_basic_auth(self, kwargs):
        """ Enforce basic authentication """
        auth_header = self.request.headers.get('Authorization')
        if auth_header is None or not auth_header.startswith('Basic '):
            self.set_unauthorized_headers()
            return False

        auth_decoded = base64.decodebytes(bytes(auth_header[6:], encoding='utf-8'))
        user, passwd = auth_decoded.split(b':', 2)
        if self.authenticate_api_user(user.decode(), passwd.decode()):
            return True

        self.set_unauthorized_headers()
        return False

    def authenticate_api_user(self, user, passwd):
        return self.account_db.authenticate_api_user(user, passwd)


class APIAccountHandler(APIHandler):
    @tornado.web.asynchronous
    def get(self):
        email = self.get_argument('email', None)

        if email is not None:
            self.account_db.get_account(email, self.got_account)
        else:
            self.got_account(None)

    @tornado.web.asynchronous
    def post(self):
        email = self.get_argument('email', 'No data received')

        self.account_db.get_account(email, self.got_account)

    def got_account(self, account):
        result = {}
        if account is not None:
            result['account_id'] = account['account_id']
            result['account_email'] = account.get('account_email')
            result['skritter_user'] = account.get('skritter_user', '')
            result['skritter_token'] = account.get('skritter_token', '')

            self.write(json.dumps(result))
        else:
            # TODO(gmwils): set an error code
            self.write(json.dumps(result))

        self.finish()


def normalize_word_array(word):
    zi, pinyin, definitions = word
    definitions = [unicodedata.normalize('NFC', definition) for definition in definitions]

    return [unicodedata.normalize('NFC', zi),
            unicodedata.normalize('NFC', pinyin),
            definitions]


class APIListHandler(APIHandler):
    def initialize(self, account_db, list_db):
        self.account_db = account_db
        self.list_db = list_db

    @tornado.web.asynchronous
    def post(self):
        body_str = self.request.body.decode('utf-8')
        body_json = json.loads(body_str)
        list_name = body_json.get('title', None)
        words = body_json.get('words', None)
        account_id = body_json.get('account_id', None)

        if list_name is None:
            self.created_list(False, 'Missing title')
            return

        if words is None or len(words) == 0:
            self.created_list(False, 'No word list supplied')
            return

        if account_id is None:
            self.created_list(False, 'Account id required')
            return

        words = [normalize_word_array(word) for word in words]

        cb = functools.partial(self.on_list_exists,
                               list_name,
                               words,
                               account_id)

        self.list_db.list_exists_for_account(list_name, account_id, cb)

    def on_list_exists(self, list_name, words, account_id, list_id=None):
        self.list_db.create_list(list_name, words, self.created_list,
                                 list_id, account_id=account_id)

    def created_list(self, success, reason=None, list_id=None):
        params = {}
        if success:
            self.set_status(201)
            if list_id is not None:
                params['list_id'] = list_id
                params['list_path'] = '/list/%d.html' % list_id

        else:
            self.set_status(500)
            if reason is not None:
                params['error'] = 'Error: %s' % reason
            else:
                params['error'] = 'Failed to create list.'

        self.set_header('Content-Type', 'application/json; charset=UTF-8')
        self.write(json.dumps(params))
        self.finish()

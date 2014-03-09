# -*- coding: utf-8 -*-
# Copyright (c) 2014 Geoff Wilson <gmwils@gmail.com>

from base64 import b64encode
from cihui.handler import common
from datetime import datetime, timedelta
from tornado import gen

import json
import logging
import tornado.httpclient
import tornado.web
import urllib.parse


class AuthHandler(common.BaseHandler):
    def initialize(self, account_db, client_id, client_secret, redirect_uri):
        self.account_db = account_db
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri

    @tornado.web.asynchronous
    def get(self, action=None):
        if action == 'get':
            params = {
                'response_type': 'code',
                'client_id': self.client_id,
                'redirect_uri': self.redirect_uri,
                }
            data = urllib.parse.urlencode(params)
            self.redirect('https://www.skritter.com/api/v0/oauth2/authorize?%s' % data)

        elif action == 'auth':
            code = self.get_argument('code', None)
            if code is None:
                # TODO(gmwils): show info to user on error
                self.redirect('/')
                return

            # Request OAuth token from Skritter
            client = tornado.httpclient.AsyncHTTPClient()
            params = {
                'grant_type': 'authorization_code',
                'client_id': self.client_id,
                'client_secret': self.client_secret,
                'redirect_uri': self.redirect_uri,
                'code': code
                }

            data = urllib.parse.urlencode(params)
            token_url = 'https://www.skritter.com/api/v0/oauth2/token?%s' % data
            credentials = '%s:%s' % (self.client_id, self.client_secret)
            credentials = b'basic ' + b64encode(credentials.encode('utf-8'))

            headers = {'AUTHORIZATION': credentials}
            client.fetch(token_url, self.handle_token, headers=headers)

        else:
            self.redirect('/')

    @tornado.web.asynchronous
    @gen.engine
    def handle_token(self, response):
        if response.error or response.code != 200:
            logging.error('Error requesting Skritter OAuth token: %s', response.error)
            self.redirect('/')
            return

        token_response = json.loads(response.body.decode('utf-8'))

        user_id = token_response.get('user_id')
        access_token = token_response.get('access_token')
        expires_in = token_response.get('expires_in', 0)
        refresh_token = token_response.get('refresh_token')
        expiry_date = datetime.utcnow() + timedelta(seconds=expires_in)

        error = yield gen.Task(self.account_db.store_skritter_token,
                               self.current_user,
                               user_id,
                               access_token,
                               refresh_token,
                               expiry_date)

        if error is None:
            self.redirect('/user/%s' % self.current_user)
        else:
            self.redirect('/')

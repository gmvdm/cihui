# -*- coding: utf-8 -*-
# Copyright (c) 2012 Geoff Wilson <gmwils@gmail.com>

from cihui.data import base

import base64
import functools
import hashlib
import hmac
import os


def build_password_digest(password, salt):
    password_hash = hashlib.sha256(salt.encode() + password.encode())
    password_digest = base64.b64encode(password_hash.digest())

    return password_digest


class AccountData(base.AsyncDatabase):
    def __init__(self, db_url, db=None):
        super(AccountData, self).__init__(db_url, db)

    def authenticate_api_user(self, user, passwd):
        valid_user = os.environ.get('API_USER', 'user')
        valid_passwd = os.environ.get('API_PASS', 'secret')

        return (user == valid_user and passwd == valid_passwd)

    def authenticate_web_user(self, user, passwd, next_url, callback):

        cb_id = self.add_callback(callback, user)
        cb = functools.partial(self._on_authenticate_web_user, passwd, next_url, cb_id)
        self.db.execute('SELECT id, email, password_hash, password_salt FROM account WHERE email = %s', (user,),
                        callback=cb)

    def _on_authenticate_web_user(self, passwd, next_url, cb_id, cursor, error=None):
        callback, user = self.get_callback(cb_id)

        if error is not None or cursor is None or cursor.rowcount == 0:
            callback()
            return

        result = cursor.fetchone()
        if result is not None and len(result) > 3:
            account_id = result[0]
            account_email = result[1]
            password_hash = result[2]
            password_salt = result[3]

            current_digest = build_password_digest(passwd, password_salt)

            if hmac.compare_digest(password_hash.encode(), current_digest):
                # TODO(gmwils): return user id instead of email
                callback(account_id, next_url, account_email)
                return

        callback()

    def get_account(self, email, callback):
        cb_id = self.add_callback(callback, email)
        cb = functools.partial(self._on_get_account_response, cb_id)

        self.db.execute('SELECT id, email, created_at, modified_at FROM account WHERE email = %s;',
                        (email,),
                        callback=cb)

    def _on_get_account_response(self, cb_id, cursor, error=None):
        callback, email = self.get_callback(cb_id)

        if cursor is None or cursor.rowcount == 0:
            callback(None)

        result = cursor.fetchone()
        response = {}

        if result is not None and len(result) >= 4:
            response['account_id'] = result[0]
            response['account_email'] = result[1]
            response['created_at'] = result[2]
            response['modified_at'] = result[3]

        callback(response)

    def create_account(self, email, passwd, callback):
        cb_id = self.add_callback(callback, email)
        cb = functools.partial(self._on_create_account_response, cb_id)

        # See: https://crackstation.net/hashing-security.htm
        passwd_salt = base64.b64encode(os.urandom(64)).decode()
        passwd_digest = build_password_digest(passwd, passwd_salt)

        self.db.execute('INSERT INTO account (email, password_hash, password_salt) VALUES (%s, %s, %s) RETURNING id',
                        (email, passwd_digest.decode(), passwd_salt),
                        callback=cb)

    def _on_create_account_response(self, cb_id, cursor, error=None):
        callback, email = self.get_callback(cb_id)

        if cursor is None or cursor.rowcount == 0:
            callback(None)
        else:
            user_id = cursor.fetchone()[0]
            callback(user_id)

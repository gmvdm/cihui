# -*- coding: utf-8 -*-
# Copyright (c) 2012 Geoff Wilson <gmwils@gmail.com>

from cihui import database_url
import json
import logging
import momoko
import os


class BaseDatabase(object):
    def __init__(self):
        self.callback_counter = 0
        # TODO(gmwils): Ensure the dict doesn't grow forever. Compact somehow
        self.callbacks = {}

    def add_callback(self, cb, rock=''):
        cb_counter = self.callback_counter
        self.callback_counter += 1
        cb_id = '%d|%s' % (cb_counter, rock)

        self.callbacks[cb_id] = cb

        return cb_id

    def get_callback(self, cb_id):
        callback = self.callbacks.get(cb_id, None)
        _, rock = cb_id.split('|', 2)

        if callback is not None:
            del self.callbacks[cb_id]

        return callback, rock


class AsyncDatabase(BaseDatabase):
    def __init__(self, db_url, db=None):
        super(AsyncDatabase, self).__init__()

        if db is not None:
            self.db = db
        else:
            settings = database_url.build_settings_from_dburl(db_url)
            self.db = momoko.AsyncClient(settings)


# TODO(gmwils) refactor into multiple stores (Account, List)
class Database(AsyncDatabase):
    def __init__(self, db_url, db=None):
        super(Database, self).__init__(db_url, db)

    def authenticate_api_user(self, user, passwd):
        valid_user = os.environ.get('API_USER', 'user')
        valid_passwd = os.environ.get('API_PASS', 'secret')

        return (user == valid_user and passwd == valid_passwd)

    def get_account(self, email, callback):
        cb_id = self.add_callback(callback, email)

        self.db.batch({cb_id: ['SELECT * FROM account WHERE email = %s;', (email,)]},
                      callback=self._on_get_account_response)

    def _on_get_account_response(self, cursors):
        for key, cursor in cursors.items():
            callback, email = self.get_callback(key)

            if len(cursor) == 0:
                callback(None)
            else:
                # TODO(gmwils) build an account object
                callback(cursor.fetchall())

    def get_lists(self, cb):
        cb_id = self.add_callback(cb)

        self.db.batch({cb_id: ['SELECT id, title FROM list ORDER BY created_at DESC;', ()]},
                      callback=self._on_get_lists_response)

    def _on_get_lists_response(self, cursors):
        for key, cursor in cursors.items():
            callback, _ = self.get_callback(key)

            if cursor is None or cursor.rowcount == 0:
                logging.warning('No lists found in database')
                callback(None)
            else:
                word_lists = []
                for word_list in cursor:
                    word_lists.append({'id': word_list[0], 'title': word_list[1]})

                callback(word_lists)

    def get_word_list(self, list_id, cb):
        cb_id = self.add_callback(cb, list_id)

        self.db.batch({cb_id: ['SELECT id, title, words FROM list WHERE id = %s;',
                               (list_id,)]},
                      callback=self._on_get_word_list_response)

    def _on_get_word_list_response(self, cursors):
        for key, cursor in cursors.items():
            callback, list_id = self.get_callback(key)

            if cursor.rowcount != 1:
                logging.warning('Invalid response for get_word_list(%s)', key)
                callback(None)
                continue

            result = cursor.fetchone()
            words = result[2]
            if words is not None:
                words = json.loads(words)

            word_list = {'id': result[0], 'title': result[1], 'words': words}
            callback(word_list)

    def create_list(self, list_name, list_elements, cb):
        cb_id = self.add_callback(cb, list_name)

        self.db.batch({cb_id: ['INSERT INTO list (title, words) VALUES (%s, %s)',
                               (list_name, json.dumps(list_elements))]},
                      callback=self._on_create_list_response)

    def _on_create_list_response(self, cursors):
        for key, cursor in cursors.items():
            callback, list_name = self.get_callback(key)

            if callback is None:
                # XXX(gmwils) should log an error here
                continue

            # TODO(gmwils) determine success/fail of insert
            callback(True)

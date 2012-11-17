# -*- coding: utf-8 -*-
# Copyright (c) 2012 Geoff Wilson <gmwils@gmail.com>

import dj_database_url
import json
import logging
import momoko


# TODO(gmwils) separate into a new file
def build_settings_from_dburl(db_url, min_conn=1, max_conn=20, cleanup_timeout=10):
    settings = {}

    db_url_settings = dj_database_url.parse(db_url)

    mapping = {'NAME': 'database',
               'HOST': 'host',
               'PORT': 'port',
               'USER': 'user',
               'PASSWORD': 'password'}

    for k, v in mapping.items():
        settings[v] = db_url_settings[k]

    settings['min_conn'] = min_conn
    settings['max_conn'] = max_conn
    settings['cleanup_timeout'] = cleanup_timeout

    return settings


# TODO(gmwils) refactor into multiple stores
class Database:
    def __init__(self, db_url, db=None):
        self.lists_counter = 0
        self.callbacks = {}
        self.list_callbacks = {}
        self.create_list_callbacks = {}
        self.get_word_list_callbacks = {}
        if db is not None:
            self.db = db
        else:
            settings = build_settings_from_dburl(db_url)
            self.db = momoko.AsyncClient(settings)

    def get_account(self, email, callback):
        self.callbacks[email] = callback
        self.db.batch({email: ['SELECT * FROM account WHERE email = %s;', (email,)]},
                      callback=self._on_get_account_response)

    def _on_get_account_response(self, cursors):
        for key, cursor in cursors.items():
            # TODO(gmwils) remove callback before calling
            # XXX(gmwils) self.callbacks could grow unbounded, may need compacting dict
            if len(cursor) == 0:
                self.callbacks[key](None)
            else:
                # TODO(gmwils) build an account object
                self.callbacks[key](cursor.fetchall())

    def get_lists(self, cb):
        counter = self.lists_counter
        self.lists_counter = counter + 1
        self.list_callbacks[counter] = cb

        self.db.batch({counter: ['SELECT id, title FROM list ORDER BY created_at DESC;', ()]},
                      callback=self._on_get_lists_response)

    def _on_get_lists_response(self, cursors):
        for key, cursor in cursors.items():
            callback = self.list_callbacks.get(key, None)
            if callback is None:
                continue

            del self.list_callbacks[key]

            if cursor is None or cursor.rowcount == 0:
                logging.warning('No lists found in database')
                callback(None)
            else:
                word_lists = []
                for word_list in cursor:
                    word_lists.append({'id': word_list[0], 'title': word_list[1]})

                callback(word_lists)

    def get_word_list(self, list_id, cb):
        self.get_word_list_callbacks[list_id] = cb
        self.db.batch({list_id: ['SELECT id, title, words FROM list WHERE id = %s;',
                                 (list_id,)]},
                      callback=self._on_get_word_list_response)

    def _on_get_word_list_response(self, cursors):
        for key, cursor in cursors.items():
            callback = self.get_word_list_callbacks.get(key, None)
            if callback is None:
                continue

            del self.get_word_list_callbacks[key]

            if cursor.rowcount != 1:
                logging.warning('Invalid response for get_word_list(%s)', key)
                callback(None)
                continue

            result = cursor.fetchone()
            word_list = {'id': result[0], 'title': result[1], 'words': result[2]}
            callback(word_list)

    def create_list(self, list_name, list_elements, cb):
        self.create_list_callbacks[list_name] = cb
        self.db.batch({list_name: ['INSERT INTO list (title, words) VALUES (%s, %s)',
                                   (list_name, json.dumps(list_elements))]},
                      callback=self._on_create_list_response)

    def _on_create_list_response(self, cursors):
        for key, cursor in cursors.items():
            callback = self.create_list_callbacks.get(key, None)

            if callback is None:
                # XXX(gmwils) should log an error here
                continue

            del self.create_list_callbacks[key]

            # TODO(gmwils) determine success/fail of insert
            callback(True)

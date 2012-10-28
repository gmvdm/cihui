# -*- coding: utf-8 -*-
# Copyright (c) 2012 Geoff Wilson <gmwils@gmail.com>

import dj_database_url
import logging
import momoko


def build_settings_from_dburl(db_url):
    settings = {}

    db_url_settings = dj_database_url.parse(db_url)

    mapping = {'NAME': 'database',
               'HOST': 'host',
               'PORT': 'port',
               'USER': 'user',
               'PASSWORD': 'password'}

    for k, v in mapping.items():
        settings[v] = db_url_settings[k]

    settings['min_conn'] = 1
    settings['max_conn'] = 20
    settings['cleanup_timeout'] = 10

    return settings


# TODO(gmwils) refactor into multiple stores
class Database:
    def __init__(self, db_url, db=None):
        self.lists_counter = 0
        self.callbacks = {}
        self.list_callbacks = {}
        if db is not None:
            self.db = db
        else:
            settings = build_settings_from_dburl(db_url)
            self.db = momoko.AsyncClient(settings)

    def get_account(self, email, callback):
        self.callbacks[email] = callback
        self.db.batch({email: ['SELECT * FROM user WHERE email = "%s";', (email,)]},
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

        self.db.batch({counter: ['SELECT * FROM list;', ()]},
                      callback=self._on_get_lists_response)

    def _on_get_lists_response(self, cursors):
        # self.list_callbacks[0]('hello')

        for key, cursor in cursors.items():
            callback = self.list_callbacks.get(key, None)
            if callback is None:
                continue

            del self.list_callbacks[key]

            if cursor is None or cursor.rowcount == 0:
                logging.warning('No lists found in database')
                callback(None)
            else:
                # TODO(gmwils) build a list of lists
                callback(cursor.fetchall())

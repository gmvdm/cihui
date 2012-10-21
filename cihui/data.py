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

    for k,v in mapping.items():
        settings[v] = db_url_settings[k]

    settings['min_conn'] = 1
    settings['max_conn'] = 20
    settings['cleanup_timeout'] = 10

    return settings

class Database:
    def __init__(self, db_url):
        settings = build_settings_from_dburl(db_url)
        self.db = momoko.AsyncClient(settings)

    def get_account(self, email, callback):
        self.db.execute('SELECT 54321;', callback=self._on_get_account_response)
        return None

    def _on_get_account_response(self, cursor):
        print cursor.fetchall()
        # self.write('Query results: %s' % cursor.fetchall())
        # self.finish()


    def get_lists(self, callback):
        self.lists_callback = callback
        # callback(self.settings)
        self.db.execute('SELECT 1, 2, 3, 4;', callback=self._on_get_lists_response)
        return None

    def _on_get_lists_response(self, cursor):
        results = cursor.fetchall()
        self.lists_callback(results)

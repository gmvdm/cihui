# -*- coding: utf-8 -*-
# Copyright (c) 2012 Geoff Wilson <gmwils@gmail.com>

import dj_database_url
import logging
import momoko



class Database:
    def __init__(self, db_url):
        settings = {}
        logging.info("Database url: %s", db_url)

        db_url_settings = dj_database_url.parse(db_url)
        settings['database'] = db_url_settings['NAME']
        settings['host'] = db_url_settings['HOST']
        settings['port'] = db_url_settings['PORT']
        settings['user'] = db_url_settings['USER']
        settings['password'] = db_url_settings['PASSWORD']

        settings['min_conn'] = 1
        settings['max_conn'] = 20
        settings['cleanup_timeout'] = 10

        self.settings = settings

        logging.info("Connecting with settings: %s", str(settings))

        self.db = momoko.AsyncClient(settings)

    def get_account(self, email, callback):
        self.db.execute('SELECT 42, 12, 40, 11;', callback=self._on_get_account_response)
        return None

    def _on_get_account_response(self, cursor):
        print cursor.fetchall()
        # self.write('Query results: %s' % cursor.fetchall())
        # self.finish()


    def get_lists(self, callback):
        self.lists_callback = callback
        # callback(self.settings)
        self.db.execute('SELECT 42, 12, 40, 11;', callback=self._on_get_lists_response)
        return None

    def _on_get_lists_response(self, cursor):
        results = cursor.fetchall()
        self.lists_callback(results)

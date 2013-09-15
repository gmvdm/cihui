# -*- coding: utf-8 -*-
# Copyright (c) 2012 Geoff Wilson <gmwils@gmail.com>

from cihui.data import base
from cihui import uri

import datetime
import functools
import json
import logging


class WordListData(base.AsyncDatabase):
    def __init__(self, db_url, db=None):
        super(WordListData, self).__init__(db_url, db)

    def get_lists(self, callback):
        cb_id = self.add_callback(callback)
        cb = functools.partial(self._on_get_lists_response, cb_id)

        self.db.execute('''SELECT id, title, stub
                           FROM list
                           WHERE public = %s
                           ORDER BY modified_at DESC;''',
                        ('true',),
                        callback=cb)

    def _on_get_lists_response(self, cb_id, cursor, error=None):
        callback, _ = self.get_callback(cb_id)

        if cursor is None or cursor.rowcount == 0:
            logging.warning('No lists found in database')
            callback(None)
        else:
            word_lists = []
            for word_list in cursor:
                word_lists.append({'id': word_list[0], 'title': word_list[1],
                                   'stub': word_list[2]})

            callback(word_lists)

    def get_word_list(self, list_id, callback):
        cb_id = self.add_callback(callback, list_id)
        cb = functools.partial(self._on_get_word_list_response, cb_id)

        self.db.execute('SELECT id, title, words, modified_at FROM list WHERE id = %s;',
                        (list_id,),
                        callback=cb)

    def _on_get_word_list_response(self, cb_id, cursor, error=None):
        callback, list_id = self.get_callback(cb_id)

        if cursor.rowcount != 1:
            logging.warning('Invalid response for get_word_list(%s)', list_id)
            callback(None)
            return

        result = cursor.fetchone()
        word_list = {}
        if len(result) > 2:
            word_list['id'] = result[0]
            word_list['title'] = result[1]
            words = result[2]
            word_list['modified_at'] = result[3]
            if words is not None:
                words = json.loads(words)

            word_list['words'] = words

        callback(word_list)

    def list_exists(self, list_name, callback):
        cb_id = self.add_callback(callback, list_name)
        cb = functools.partial(self._on_list_exists, cb_id)
        self.db.execute('SELECT max(id) FROM list WHERE title=%s', (list_name,),
                        callback=cb)

    def _on_list_exists(self, cb_id, cursor, error=None):
        callback, list_name = self.get_callback(cb_id)

        result = cursor.fetchone()
        if result is not None:
            list_id = result[0]
            callback(list_id)
        else:
            callback(None)

    def create_list(self, list_name, list_elements, callback, list_id=None, account_id=None, email_address=None):
        cb_id = self.add_callback(callback, list_id)
        cb = functools.partial(self._on_create_list_response, cb_id)

        if list_id is not None:
            self.db.execute(
                'UPDATE list SET words=%s, modified_at=%s, stub=%s WHERE id=%s AND account_id in (SELECT id FROM account WHERE id = %s or email = %s)',
                (json.dumps(list_elements),
                 datetime.datetime.now(),
                 uri.title_to_stub(list_name),
                 list_id,
                 account_id,
                 email_address),
                callback=cb)

        else:
            self.db.execute(
                'INSERT INTO list (title, words, stub, account_id) VALUES (%s, %s, %s, (SELECT id FROM account WHERE id = %s OR email = %s)) RETURNING id',
                (list_name,
                 json.dumps(list_elements),
                 uri.title_to_stub(list_name),
                 account_id,
                 email_address),
                callback=cb)

    def _on_create_list_response(self, cb_id, cursor, error=None):
        callback, list_id_str = self.get_callback(cb_id)

        if callback is None:
            # XXX(gmwils) should log an error here
            return

        if error is not None:
            callback(False)
            return

        list_id = None
        try:
            list_id = int(list_id_str)
        except ValueError:
            pass

        if list_id is None:
            result = cursor.fetchone()
            list_id = result[0]

        callback(True, list_id=list_id)

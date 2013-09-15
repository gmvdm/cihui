# -*- coding: utf-8 -*-
# Copyright (c) 2012 Geoff Wilson <gmwils@gmail.com>

from cihui.data import database_url
import momoko


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
            if settings.get('user') is not None:
                dsn = 'dbname=%s user=%s password=%s host=%s port=%s' % (
                    settings.get('database'),
                    settings.get('user', ''),
                    settings.get('password', ''),
                    settings.get('host', 'localhost'),
                    settings.get('port', 5432))
            else:
                dsn = 'dbname=%s host=%s port=%s' % (
                    settings.get('database'),
                    settings.get('host', 'localhost'),
                    settings.get('port', 5432))

            self.db = momoko.Pool(dsn)

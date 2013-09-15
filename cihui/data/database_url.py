# -*- coding: utf-8 -*-
# Copyright (c) 2012 Geoff Wilson <gmwils@gmail.com>

import dj_database_url


def build_settings_from_dburl(db_url, min_conn=1, max_conn=20, cleanup_timeout=10):
    settings = {}

    db_url_settings = dj_database_url.parse(db_url)

    mapping = {'NAME': 'database',
               'HOST': 'host',
               'PORT': 'port',
               'USER': 'user',
               'PASSWORD': 'password'}

    for k, v in list(mapping.items()):
        settings[v] = db_url_settings[k]

    settings['min_conn'] = min_conn
    settings['max_conn'] = max_conn
    settings['cleanup_timeout'] = cleanup_timeout

    return settings

# -*- coding: utf-8 -*-
# Copyright (c) 2012 Geoff Wilson <gmwils@gmail.com>

import mock
import unittest

from cihui import database_url


class TestMapDbUrl(unittest.TestCase):
    def test_simple_example(self):
        url = 'postgresql://username:pass@hostname:1234/dbname'
        expectations = {'host': 'hostname',
                        'database': 'dbname',
                        'user': 'username',
                        'password': 'pass'}
        settings = database_url.build_settings_from_dburl(url)

        for k, v in expectations.items():
            self.assertEqual(settings[k], v)

    def test_default_params(self):
        url = 'postgresql://username:pass@hostname:1234/dbname'
        settings = database_url.build_settings_from_dburl(url)
        self.assertEqual(settings['min_conn'], 1)
        self.assertEqual(settings['max_conn'], 20)
        self.assertEqual(settings['cleanup_timeout'], 10)

    def test_passedin_params(self):
        url = 'postgresql://username:pass@hostname:1234/dbname'
        settings = database_url.build_settings_from_dburl(url, max_conn=100, min_conn=5, cleanup_timeout=20)
        self.assertEqual(settings['min_conn'], 5)
        self.assertEqual(settings['max_conn'], 100)
        self.assertEqual(settings['cleanup_timeout'], 20)

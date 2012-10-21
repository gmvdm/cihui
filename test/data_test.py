# -*- coding: utf-8 -*-
# Copyright (c) 2012 Geoff Wilson <gmwils@gmail.com>

import mock
import unittest

from tornado.testing import AsyncHTTPTestCase
from cihui import data

class TestMapDbUrl(unittest.TestCase):
    def test_simple_example(self):
        url = 'postgresql://username:pass@hostname:1234/dbname'
        expectations = {'host': 'hostname',
                        'database': 'dbname',
                        'user': 'username',
                        'password': 'pass'}
        settings = data.build_settings_from_dburl(url)

        for k,v in expectations.items():
            self.assertEqual(settings[k], v)


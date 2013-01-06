# -*- coding: utf-8 -*-
# Copyright (c) 2012 Geoff Wilson <gmwils@gmail.com>

from cihui import formatter
import unittest


class TestDescriptionFormatter(unittest.TestCase):
    def test_basic_description(self):
        self.assertEqual(u'a', formatter.format_description([u'a']))

    def test_multiple_descriptions(self):
        desc = [u'a', 'b', 'c']
        self.assertEqual(u'a; b; c', formatter.format_description(desc))

    def test_example_description(self):
        desc = [u'grassland', u'prairie', u'CL:\u7247[pian4]']
        self.assertEqual(u'grassland; prairie; CL:\u7247[pian4]', formatter.format_description(desc))

# -*- coding: utf-8 -*-
# Copyright (c) 2012 Geoff Wilson <gmwils@gmail.com>

from cihui import atom_formatter
import unittest


class TestAtomFormatter(unittest.TestCase):
    def test_empty_list(self):
        self.assertIn('http://www.w3.org/2005/Atom', atom_formatter.format_atom())


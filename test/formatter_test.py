# -*- coding: utf-8 -*-
# Copyright (c) 2012 Geoff Wilson <gmwils@gmail.com>

from cihui import formatter
import unittest


class TestDescriptionFormatter(unittest.TestCase):
    def test_basic_description(self):
        self.assertEqual('a', formatter.format_description(['a']))

    def test_multiple_descriptions(self):
        desc = ['a', 'b', 'c']
        self.assertEqual('a; b; c', formatter.format_description(desc))

    def test_example_description(self):
        desc = ['grassland', 'prairie', 'CL:\u7247[pian4]']
        self.assertEqual('grassland; prairie; CL:\u7247[pian4]', formatter.format_description(desc))


class TestCSVWordFormatter(unittest.TestCase):
    def test_basic_formatting(self):
        word = ['大', 'da', ['big']]
        self.assertEqual('"大","da","big"', formatter.format_word_as_csv(word))

    def test_word_without_description(self):
        word = ['大', 'da']
        self.assertEqual('"大","da",""', formatter.format_word_as_csv(word))


class TestTabWordFormmater(unittest.TestCase):
    def test_basic_formatting(self):
        word = ['大', 'da', ['big']]
        self.assertEqual('大\tbig\tda', formatter.format_word_as_tsv(word))

    def test_word_without_description(self):
        word = ['大', 'da']
        self.assertEqual('大\t\tda', formatter.format_word_as_tsv(word))

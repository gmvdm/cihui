# -*- coding: utf-8 -*-
# Copyright (c) 2012 Geoff Wilson <gmwils@gmail.com>

import unittest

from cihui import uri


class TestURIStub(unittest.TestCase):
    def test_uri_to_stub(self):
        uri_string = uri.generate_stub(123, 'This is the list title')
        self.assertEqual(uri_string, '123-this-is-the-list-title')

    def test_no_title(self):
        uri_string = uri.generate_stub(123)
        self.assertEqual(uri_string, '123')

    def test_title_with_punctuation(self):
        uri_string = uri.generate_stub(123, '   TiTLe!#%@%  CaSE!!  ')
        self.assertEqual(uri_string, '123-title-case')

    def test_chinese_characters(self):
        uri_string = uri.generate_stub(123, u'Word List: 小禺言')
        self.assertEqual(uri_string, '123-word-list-xiao-yu-yan')


if __name__ == '__main__':
    unittest.main()

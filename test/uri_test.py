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


class TestURITitleStub(unittest.TestCase):
    def test_title_with_punctuation(self):
        stub = uri.title_to_stub('   TiTLe!#%@%  CaSE!!  ')
        self.assertEqual(stub, 'title-case')

    def test_chinese_characters(self):
        stub = uri.title_to_stub(u'Word List: 小禺言')
        self.assertEqual(stub, 'word-list-xiao-yu-yan')

    def test_non_unicode_chinese_characters(self):
        stub = uri.title_to_stub('北京')
        self.assertEqual(stub, 'bei-jing')


if __name__ == '__main__':
    unittest.main()

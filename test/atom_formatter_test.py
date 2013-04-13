# -*- coding: utf-8 -*-
# Copyright (c) 2012 Geoff Wilson <gmwils@gmail.com>

from cihui import atom_formatter
from xml.etree import ElementTree

import unittest


class TestAtomFormatter(unittest.TestCase):
    def test_empty_list(self):
        self.assertIn(b'http://www.w3.org/2005/Atom', atom_formatter.format_atom())

    def test_set_title(self):
        atom_xml = atom_formatter.format_atom(title=u'大 feed title')
        root_elem = ElementTree.fromstring(atom_xml)
        title_elem = root_elem.find('{http://www.w3.org/2005/Atom}title')

        self.assertEqual(u'大 feed title', title_elem.text)

    def test_include_single_item(self):
        entry_list = [{'title': 'Title', 'link': '/link/', 'updated': '2013-03-14T00:00:00+01:00'}]

        atom_xml = atom_formatter.format_atom(title='Feed Title', entries=entry_list)
        root_elem = ElementTree.fromstring(atom_xml)
        entry_elem = root_elem.find('{http://www.w3.org/2005/Atom}entry')

        self.assertEqual('Title', entry_elem.find('{http://www.w3.org/2005/Atom}title').text)

        link_elem = entry_elem.find('{http://www.w3.org/2005/Atom}link')
        self.assertEqual('/link/', link_elem.get('href'))

    def test_multiple_items(self):
        entry_list = [{'title': 'First'}, {'title': 'Second'}]
        atom_xml = atom_formatter.format_atom(entries=entry_list)

        root_elem = ElementTree.fromstring(atom_xml)
        entries = root_elem.findall('{http://www.w3.org/2005/Atom}entry')

        self.assertEqual(2, len(entries))

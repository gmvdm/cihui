# -*- coding: utf-8 -*-
# Copyright (c) 2012 Geoff Wilson <gmwils@gmail.com>


from xml.etree import ElementTree


def format_atom(title=None, entries=[]):
    feed_elem = ElementTree.Element('feed', {'xmlns': 'http://www.w3.org/2005/Atom'})
    if title:
        title_elem = ElementTree.SubElement(feed_elem, 'title')
        title_elem.text = title

    for entry in entries:
        entry_elem = ElementTree.SubElement(feed_elem, 'entry')
        for key, value in entry.items():
            if key == 'link':
                link_elem = ElementTree.SubElement(entry_elem, key,
                                                   {'href': value,
                                                    'rel': 'alternate'})
            else:
                sub_elem = ElementTree.SubElement(entry_elem, key)
                sub_elem.text = value

    return ElementTree.tostring(feed_elem, encoding='utf-8')

# -*- coding: utf-8 -*-
# Copyright (c) 2012 Geoff Wilson <gmwils@gmail.com>


from xml.etree import ElementTree


def format_atom():
    feed_elem = ElementTree.Element('feed', {'xmlns': 'http://www.w3.org/2005/Atom'})

    return ElementTree.tostring(feed_elem)

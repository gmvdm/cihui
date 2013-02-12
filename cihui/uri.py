# -*- coding: utf-8 -*-
# Copyright (c) 2012 Geoff Wilson <gmwils@gmail.com>

import re
import unidecode


def generate_stub(id, title=None):
    "Given a numerical id and a title, generate a stub"
    stub = '%s' % (id,)

    if title is not None:
        stub += '-' + title_to_stub(title)

    return stub


def title_to_stub(title):
    "Given a multilingual title, generate a uri suitable stub"
    if type(title) == str:
        title_stub = title.decode('utf-8')
    else:
        title_stub = title

    title_stub = unidecode.unidecode(title_stub)

    title_stub = title_stub.lower().strip()

    split_title = re.split(r'\s+', title_stub)

    stub = '-'.join(split_title)
    stub = re.sub(r'[^\w\-]+', '', stub)
    stub = re.sub(r'-+$', '', stub)

    return stub


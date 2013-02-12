# -*- coding: utf-8 -*-
# Copyright (c) 2012 Geoff Wilson <gmwils@gmail.com>

import re
import unidecode


def generate_stub(id, title=None):
    stub = '%s' % (id,)
    if title is not None:
        title_stub = unidecode.unidecode(title)
        title_stub = title_stub.lower()
        title_stub = title_stub.strip()

        split_title = re.split(r'\s+', title_stub)

        stub += '-' + '-'.join(split_title)
        stub = re.sub(r'[^\w\-]+', '', stub)
        stub = re.sub(r'-+$', '', stub)

    return stub

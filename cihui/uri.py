# -*- coding: utf-8 -*-
# Copyright (c) 2012 Geoff Wilson <gmwils@gmail.com>

import re


def generate_stub(id, title=None):
    stub = '%s' % (id,)
    if title is not None:
        title = title.lower()
        title = title.strip()

        split_title = re.split(r'\s+', title)

        stub += '-' + '-'.join(split_title)
        stub = re.sub(r'[^\w\-]+', '', stub)
        stub = re.sub(r'-+$', '', stub)

    return stub

#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2012 Geoff Wilson <gmwils@gmail.com>

import json
import requests


if __name__ == '__main__':
    payload = {'title': 'Scrpt List', 'words': [[u'大', u'dà', ['big']],
                                                 [u'小', u'xiao', ['small']]]}
    r = requests.post('http://localhost:5000/api/list',
                      data=json.dumps(payload),
                      auth=('user', 'secret'))

    print r.text

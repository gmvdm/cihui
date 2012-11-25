#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2012 Geoff Wilson <gmwils@gmail.com>

import json
import requests


if __name__ == '__main__':
    payload = {'title': 'Script List', 'words': [[u'大', u'dà', 'big'], ]}
    r = requests.post('http://localhost:5000/api/list',
                      data=json.dumps(payload),
                      auth=('user', 'secret'))

    print r.text

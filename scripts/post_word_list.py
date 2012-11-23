#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2012 Geoff Wilson <gmwils@gmail.com>

import json
import requests


if __name__ == '__main__':
    payload = {'list': 'Script List', 'words': json.dumps([(u'大', 'da', 'big'), ])}
    # payload = {'list': 'Script List', 'words': ''}
    r = requests.post('http://localhost:5000/api/list', data=payload)

    print r.text

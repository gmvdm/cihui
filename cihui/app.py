# -*- coding: utf-8 -*-
# Copyright (c) 2012 Geoff Wilson <gmwils@gmail.com>

from cihui.handler import api
from cihui.handler import auth
from cihui.handler import wordlist
from cihui.handler import user

import os
import tornado.web


class CiHuiApplication(tornado.web.Application):
    def __init__(self,
                 account_database,
                 list_database,
                 cookie_secret=None,
                 debug=False):

        self.account_db = account_database
        self.list_db = list_database

        settings = {'static_path': os.path.join(os.path.dirname(__file__), '../static'),
                    'template_path': os.path.join(os.path.dirname(__file__), '../templates'),
                    'xsrf_cookies': True,
                    'debug': debug,
                    'login_url': '/login'
                    }

        if cookie_secret is None:
            settings['cookie_secret'] = 'Crouching Tiger, Hidden Dragon'
        else:
            settings['cookie_secret'] = cookie_secret

        handlers = [(r'/', wordlist.MainHandler, dict(list_db=self.list_db)),
                    (r'/api/account', api.APIAccountHandler, dict(account_db=self.account_db)),
                    (r'/api/list', api.APIListHandler, dict(account_db=self.account_db, list_db=self.list_db)),

                    (r'/atom.xml', wordlist.AtomHandler, dict(list_db=self.list_db)),
                    (r'/login', auth.LoginHandler, dict(account_db=self.account_db)),
                    (r'/logout', auth.LogoutHandler),
                    tornado.web.url(r'/list/([0-9]+)[^\.]*(\.?\w*)', wordlist.WordListHandler, dict(list_db=self.list_db), name='list'),
                    (r'/user/(\w+)$', user.UserHandler, dict(account_db=self.account_db)),
                    (r'/user', user.UserHandler, dict(account_db=self.account_db)),
                    ]

        tornado.web.Application.__init__(self, handlers, **settings)

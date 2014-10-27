# -*- coding: utf-8 -*-
# Copyright (c) 2012-2014 Geoff Wilson <gmwils@gmail.com>

from cihui.handler import api
from cihui.handler import auth
from cihui.handler import skritter
from cihui.handler import wordlist
from cihui.handler import user
from cihui import uimodules

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

        self.skritter_client_id = os.environ.get('SKRITTER_OAUTH_CLIENT_ID')
        self.skritter_client_secret = os.environ.get('SKRITTER_OAUTH_CLIENT_SECRET')
        self.skritter_redirect_uri = os.environ.get('SKRITTER_REDIRECT_URI')

        settings = {'static_path': os.path.join(os.path.dirname(__file__), '../static'),
                    'template_path': os.path.join(os.path.dirname(__file__), '../templates'),
                    'xsrf_cookies': True,
                    'debug': debug,
                    'login_url': '/login',
                    'ui_modules': uimodules
                    }

        if cookie_secret is None:
            settings['cookie_secret'] = 'Crouching Tiger, Hidden Dragon'
        else:
            settings['cookie_secret'] = cookie_secret

        handlers = [(r'/', wordlist.IndexHandler, dict(list_db=self.list_db)),
                    (r'/home', wordlist.HomeHandler, dict(list_db=self.list_db)),
                    (r'/skritter/(\w+)$', skritter.AuthHandler,
                     dict(account_db=self.account_db,
                          client_id=self.skritter_client_id,
                          client_secret=self.skritter_client_secret,
                          redirect_uri=self.skritter_redirect_uri)),
                    (r'/api/account', api.APIAccountHandler,
                     dict(account_db=self.account_db)),
                    (r'/api/account/skritter$', api.APIAccountSkritterHandler,
                     dict(account_db=self.account_db,
                          client_id=self.skritter_client_id,
                          client_secret=self.skritter_client_secret,
                          redirect_uri=self.skritter_redirect_uri)),
                    (r'/api/list', api.APIListHandler,
                     dict(account_db=self.account_db,
                          list_db=self.list_db)),
                    (r'/atom.xml', wordlist.AtomHandler,
                     dict(list_db=self.list_db)),
                    (r'/login', auth.LoginHandler,
                     dict(account_db=self.account_db)),
                    (r'/logout', auth.LogoutHandler),
                    tornado.web.url(r'/list/([0-9]+)[^\.]*(\.?\w*)', wordlist.WordListHandler,
                                    dict(list_db=self.list_db),
                                    name='list'),
                    (r'/user/(\w+)$', user.UserHandler,
                     dict(account_db=self.account_db)),
                    (r'/user/(\w+)/(\w+)$', user.UserHandler,
                     dict(account_db=self.account_db)),
                    (r'/user', user.UserHandler,
                     dict(account_db=self.account_db)),
                    ]

        tornado.web.Application.__init__(self, handlers, **settings)

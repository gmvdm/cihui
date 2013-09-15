# -*- coding: utf-8 -*-
# Copyright (c) 2012 Geoff Wilson <gmwils@gmail.com>

import tornado.web


class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        # TODO(gmwils): refactor & test
        session_key = self.get_secure_cookie('session_id')
        if session_key:
            user_id, username = str(session_key, encoding='ascii').split('|')
            return user_id

        return None

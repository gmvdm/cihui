# -*- coding: utf-8 -*-
# Copyright (c) 2014 Geoff Wilson <gmwils@gmail.com>

import tornado.web


class WordEntry(tornado.web.UIModule):
    def render(self, zi, pinyin, description):
        return self.render_string(
            "modules/wordentry.html",
            zi=zi,
            pinyin=pinyin,
            description=description)

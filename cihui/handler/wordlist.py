# -*- coding: utf-8 -*-
# Copyright (c) 2012 Geoff Wilson <gmwils@gmail.com>

import tornado.web

from cihui import atom_formatter
from cihui import formatter
from cihui.handler import common

from tornado import gen


class BaseListHandler(common.BaseHandler):
    def initialize(self, list_db):
        self.list_db = list_db

    def format_wordlists(self, word_lists):
        if word_lists is None:
            return []

        def add_stub(word_list):
            word_list['stub'] = make_stub(word_list.get('id'),
                                          word_list.get('stub'))
            return word_list

        return list(map(add_stub, word_lists))


def make_stub(list_id, stub=''):
    if stub:
        return '%s-%s' % (list_id, stub)

    return list_id


class IndexHandler(BaseListHandler):
    @tornado.web.asynchronous
    @gen.engine
    def get(self):
        if self.current_user:
            self.redirect('/home')
            return

        word_lists = yield gen.Task(self.list_db.get_lists)
        word_lists = self.format_wordlists(word_lists)

        self.render('index.html', word_lists=word_lists)


class HomeHandler(BaseListHandler):
    @tornado.web.asynchronous
    @gen.engine
    def get(self):
        if not self.current_user:
            self.redirect('/')
            return

        word_lists = yield gen.Task(self.list_db.get_user_lists,
                                    self.current_user)
        word_lists = self.format_wordlists(word_lists)

        self.render('home.html', word_lists=word_lists)


class AtomHandler(BaseListHandler):
    @tornado.web.asynchronous
    @gen.engine
    def get(self):
        word_lists = yield gen.Task(self.list_db.get_lists)
        entry_list = []
        for word_list in word_lists:
            entry = {'title': word_list.get('title'),
                     'link': '/list/%s' % make_stub(word_list.get('id'),
                                                    word_list.get('stub'))}
            entry_list.append(entry)

        self.write(atom_formatter.format_atom(title='CiHui',
                                              entries=entry_list))
        self.finish()


def add_description(entry):
    if entry is not None:
        entry.append(formatter.format_description(entry[2]))
    return entry


class WordListHandler(BaseListHandler):
    @tornado.web.asynchronous
    @gen.coroutine
    def get(self, list_id, list_format):
        word_list = yield gen.Task(self.list_db.get_word_list, int(list_id))

        if list_format == '.csv':
            self.set_content_header('text/csv')

            for word in word_list['words']:
                self.write('%s\n' % (formatter.format_word_as_csv(word)))
            self.finish()

        elif list_format == '.tsv':
            self.set_content_header('text/tsv')

            for word in word_list['words']:
                self.write('%s\n' % (formatter.format_word_as_tsv(word)))
            self.finish()

        elif word_list is not None:  # html list
            words = word_list.get('words', [])
            words = list(map(add_description, words))
            word_count = len(words)

            base_uri = self.get_base_uri()

            self.render('word_list.html',
                        title=word_list.get('title', ''),
                        word_list_id=word_list.get('id', 0),
                        modified_at=word_list.get('modified_at'),
                        words=words,
                        word_count=word_count,
                        base_uri=base_uri)
        else:
            self.send_error(404)

    def set_content_header(self, content_type='text/csv'):
        self.set_header('Content-Type', '%s; charset=utf-8' % content_type)
        self.set_status(200)

    def get_base_uri(self):
        # TODO(gmwils): build filename from canonical representation
        base_uri = self.request.path.lower()
        if base_uri.endswith('.html'):
            base_uri = base_uri[0:-5]
        elif base_uri.endswith('.htm'):
            base_uri = base_uri[0:-4]

        return base_uri

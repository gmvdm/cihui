# -*- coding: utf-8 -*-
# Copyright (c) 2012 Geoff Wilson <gmwils@gmail.com>


def format_description(desc):
    return '; '.join(desc)


def format_word_as_csv(word):
    description = ''
    if len(word) > 2:
        description = format_description(word[2])
    return u'"%s","%s","%s"' % (word[0], word[1], description)


def format_word_as_tsv(word):
    description = ''
    if len(word) > 2:
        description = format_description(word[2])
    return u'%s\t%s\t%s' % (word[0], description, word[1])

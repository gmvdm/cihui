# -*- coding: utf-8 -*-
# Copyright (c) 2012 Geoff Wilson <gmwils@gmail.com>

import os
import tornado.ioloop

from cihui import app, data

if __name__ == "__main__":
    db_url = os.environ.get('DATABASE_URL', 'postgresql://localhost:5432/cihui')
    port = int(os.environ.get("PORT", 5000))
    application = app.CiHuiApplication(data.Database(db_url),
                                       os.environ.get('COOKIE_SECRET', None))
    application.listen(port)
    tornado.ioloop.IOLoop.instance().start()


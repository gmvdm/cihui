# -*- coding: utf-8 -*-
# Copyright (c) 2012 Geoff Wilson <gmwils@gmail.com>

import os
import sys
import tornado.ioloop

from cihui import app, data

if __name__ == "__main__":
    db_url = os.environ.get('DATABASE_URL', 'postgresql://localhost:5432/cihui')
    port = int(os.environ.get("PORT", 5000))
    debugMode = False

    if len(sys.argv) > 1 and sys.argv[1] == '--debug':
        debugMode = True

    application = app.CiHuiApplication(data.AccountData(db_url),
                                       data.ListData(db_url),
                                       os.environ.get('COOKIE_SECRET', None),
                                       debug=debugMode
                                       )
    application.listen(port)
    tornado.ioloop.IOLoop.instance().start()

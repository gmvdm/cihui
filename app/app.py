# -*- coding: utf-8 -*-
# Copyright (c) 2012 Geoff Wilson <gmwils@gmail.com>

import os
import tornado.ioloop

from cihui import app

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    application = app.CiHuiApplication()
    application.listen(port)
    tornado.ioloop.IOLoop.instance().start()


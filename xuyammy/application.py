#!/usr/bin/env python

from django.conf import settings as django_settings

import tornado.ioloop
import tornado.web
import settings

django_settings.configure(
        DATABASE_ENGINE = settings.DATABASE['DATABASE_ENGINE'],
        DATABASE_NAME = settings.DATABASE['DATABASE_NAME']
)

application_settings = {
    "static_path": settings.STATIC_PATH,
    "login_url": settings.LOGIN_URL,
    "xsrf_cookies": False,
}

import urls
application = tornado.web.Application(urls.ROUTES, **application_settings)

if __name__ == "__main__":
    application.listen(settings.PORT)
    tornado.ioloop.IOLoop.instance().start()
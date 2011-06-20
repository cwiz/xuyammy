import tornado.ioloop
import tornado.web
import os


from django.conf import settings

settings.configure(
        DATABASE_ENGINE = 'django.db.backends.sqlite3',
        DATABASE_NAME = 'django.db.backends.sqlite3',
)

from dashboard.handlers import MainDashboardHandler, AjaxDashboardHandler

from django.db import models
from dashboard.models import *

settings = {
    "static_path": os.path.join(os.path.dirname(__file__), "static"),
    "cookie_secret": "61oETzKXQAGaYdkL5gEmGeJJ666h7EQnp2XdTP1o/Vo=",
    "login_url": "/login",
    "xsrf_cookies": True,
}
application = tornado.web.Application([
   (r"/", MainDashboardHandler),
   (r"/data/", AjaxDashboardHandler),
], **settings)

s = Story()
s.title = 'dsfsd'
s.description = 'dsfsdfs'
s.save()


if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
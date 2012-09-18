# -*- coding: utf-8 -*-
import os
from google.appengine.dist import use_library
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
use_library('django', '1.2')

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app


# Load request handlers
import handlers

# Map url's to handlers
urls = [(r'/', handlers.main.Main),
        (r'/oauth/callback', handlers.main.CallbackPage),
        (r'/nomfeed', handlers.main.GetNomFeed)
        ]

application = webapp.WSGIApplication(urls, debug=True)


def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()

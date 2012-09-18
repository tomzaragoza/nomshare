# -*- coding: utf-8 -*-
import os
import logging

from hashlib import md5
from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.ext.webapp import RequestHandler, template
from baserequesthandler import BaseRequestHandler

import tweepy
from oauth.models import OAuthToken
import pickle


consumer_key = 'deleted for safety reasons'
consumer_secret = 'deleted for safety reasons'
callback_url = 'deleted for safety reasons'

# Main page request handler
class Main(BaseRequestHandler):
    def get(self):
        # Render the template
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret, callback_url)

        try:
            redirect_url = auth.get_authorization_url()

            self.render("index.html", {'authurl': redirect_url,
                                       'request_token': auth.request_token})
        except tweepy.TweepError, e:
            # Failed to get a request token
            self.render('error.html', {'message': e})
            return

        # We must store the request token for later use in the callback page.
        request_token = OAuthToken(
                token_key = auth.request_token.key,
                token_secret = auth.request_token.secret
        )
        request_token.put()
        
        

# Callback page (/oauth/callback)
class CallbackPage(BaseRequestHandler):

    def get(self):
        oauth_token = self.request.get("oauth_token", None)
        oauth_verifier = self.request.get("oauth_verifier", None)
        if oauth_token is None:
            # Invalid request!
            self.render('error.html', {
                    'message': 'Missing required parameters!'
            })
            return

        # Lookup the request token
        request_token = OAuthToken.gql("WHERE token_key=:key", key=oauth_token).get()
        if request_token is None:
            # We do not seem to have this request token, show an error.
            self.render('error.html', {'message': 'Invalid token!'})
            return

        # Rebuild the auth handler
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_request_token(request_token.token_key, request_token.token_secret)

        # Fetch the access token
        try:
            auth.get_access_token(oauth_verifier)
        except tweepy.TweepError, e:
            # Failed to get access token
            self.render('error.html', {'message': e})
            return

        # So now we could use this auth handler.

        api = tweepy.API(auth)
        auth_user = api.user_timeline()[0].user.screen_name
        user_img = api.me().__getstate__()["profile_image_url_https"]
        
        self.render('callback.html', {
            'access_token': auth.access_token,
            'auth_user': auth_user,
            'user_img': user_img})

        
class GetNomFeed(BaseRequestHandler):
    
    def post(self):
        # Rebuild the auth handler
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret, callback_url)

        api = tweepy.API(auth)
        
        # variable for one line string of status updates
        statuses = ""

        user = self.request.get('username')
        
        self.render("nomfeed.html", {'statuses': statuses,
                                     'username': user})
            

    


    
    
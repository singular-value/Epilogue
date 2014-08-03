import os
import urllib, cgi

import jinja2
import webapp2
from models import User
me = User()

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class MainPage(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render({'message': "index"}))


class LoginPage(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENVIRONMENT.get_template('main.html')
        self.response.write(template.render({'message': "login"}))


class FuneralPage(webapp2.RequestHandler):
    def get(self):
        #print 'FUCK YES THIS WORKS: ' + me.dead_name
        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render({'message': "funeral"}))


class SocialPage(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render({'message': "social"}))


class FinancePage(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render({'message': "finance"}))


class MembershipPage(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render({'message': "membership"}))

class Store(webapp2.RequestHandler):
    def post(self):
        print self.request
        me.email = self.request.get('email')
        me.dead_name = self.request.get('dead_name')
        self.redirect('/funeral') #TAKE THEM TO THE NEXT PAGE HERE


application = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/login', LoginPage),
    ('/funeral', FuneralPage),
    ('/social', SocialPage),
    ('/finance', FinancePage),
    ('/memberships', MembershipPage),
    ('/store', Store)
], debug=True)
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
        template = JINJA_ENVIRONMENT.get_template('mainpageform.html')
        self.response.write(template.render({'message': "index"}))


class CertificatePage(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENVIRONMENT.get_template('certificate.html')
        self.response.write(template.render({'message': "certificate"}))


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


class UploadCertificate(webapp2.RequestHandler):
    def post(self):
        self.redirect('/certificate-form')


class CertificateForm(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENVIRONMENT.get_template('certificateform.html')
        self.response.write(template.render({"user": me}))

application = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/certificate', CertificatePage),
    ('/funeral', FuneralPage),
    ('/social', SocialPage),
    ('/finance', FinancePage),
    ('/memberships', MembershipPage),
    ('/store', Store),
    ('/certificate-upload', UploadCertificate),
    ('/certificate-form', CertificateForm),
], debug=True)
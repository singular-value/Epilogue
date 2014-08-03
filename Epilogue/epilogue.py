import os, lob
import urllib, cgi

import jinja2
import webapp2

lob.api_key = 'test_3aa918f64396a4f31c68c80f3238a617d8f'
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

## ORDER: MAINPAGE->LOGINPAGE -> ??
class LoginPage(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENVIRONMENT.get_template('main.html')
        myAddress = lob.Address.create(
            name=me.name,
            address_line1=me.address,
            address_city=me.city,
            address_state=me.state,
            address_country=me.country,
            address_zip=me.zip
        )

        # address of people / organizations to send
        yourAddress = lob.Address.create(
            name='Hoe Smith',
            address_line1='104, Printing Boulevard',
            address_city='Boston',
            address_state='MA',
            address_country='US',
            address_zip='12345'
        )

        # pre-made letter that will be sent to businesses
        letter = lob.Object.create(
            name='Letter',
            file=open('Letter.pdf','rb'),
            setting_id='100',
            quantity=1
        )

        certificate = lob.Object.create(
            name='Death Certificate',
            file=open('Letter.pdf','rb'),
            setting_id='100',
            quantity=1
        )

        job = lob.Job.create(
            name='Send out',
            to_address=yourAddress,
            from_address=myAddress,
            objects = [certificate,letter]
        )

        print job

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
        me.name = 'meeee'
        me.email = self.request.get('email')
        me.dead_name = self.request.get('dead_name')

        me.address = self.request.get('address')
        me.city = self.request.get('city')
        me.state = self.request.get('state')
        me.country = self.request.get('country')
        me.zip = self.request.get('zip')

        self.redirect('/login') #TAKE THEM TO THE NEXT PAGE HERE


application = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/login', LoginPage),
    ('/funeral', FuneralPage),
    ('/social', SocialPage),
    ('/finance', FinancePage),
    ('/memberships', MembershipPage),
    ('/store', Store)
], debug=True)
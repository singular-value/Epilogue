import os, lob
import urllib, cgi

import jinja2
import webapp2
from google.appengine.api import users

lob.api_key = 'test_3aa918f64396a4f31c68c80f3238a617d8f'
from models import User
me = User()
status = 0

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

providers = {
    'Google'   : 'https://www.google.com/accounts/o8/id',
    'Yahoo'    : 'yahoo.com',
    'MySpace'  : 'myspace.com',
    'AOL'      : 'aol.com',
    'MyOpenID' : 'myopenid.com'
    # add more here
}

class MainPage(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user:  # signed in already
            #self.response.out.write('Hello <em>%s</em>! [<a href="%s">sign out</a>]' % (
            #    user.nickname(), users.create_logout_url(self.request.uri)))
            self.redirect('/cert')
        else:     # let user choose authenticator
            self.response.out.write('Hello world! Sign in at: ')
            for name, uri in providers.items():
                self.response.out.write('[<a href="%s">%s</a>]' % (
                    users.create_login_url(federated_identity=uri), name))

class MainPage2(webapp2.RequestHandler):
    def get(self):
         template = JINJA_ENVIRONMENT.get_template('mainpageform.html')
         self.response.write(template.render({'message': "index"}))


class CertificatePage(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENVIRONMENT.get_template('certificate.html')
        self.response.write(template.render({'message': "certificate"}))


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
        if me.company is 'Twitter':
            yourAddress = lob.Address.create(
                name='Hoe Smith',
                address_line1='104, Printing Boulevard',
                address_city='Boston',
                address_state='MA',
                address_country='US',
                address_zip='12345'
            )
        elif me.company is 'PayPal':
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
        template = JINJA_ENVIRONMENT.get_template('social.html')
        self.response.write(template.render({'message': "social media cancellation"}))


class FinancePage(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENVIRONMENT.get_template('finance.html')
        self.response.write(template.render({'message': "finance", 'page_num':1}))

class FinancePage2(webapp2.RequestHandler):
    def get(self):
        self.response.write('Call THIS NUMBER to cancel with ' + me.bank)
        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render({'message': "finance","bank":me.bank}))
        # to do later: use the bank in the actual html

class MembershipPage(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render({'message': "membership"}))

#stores which banks the user uses
class StoreBank(webapp2.RequestHandler):
    def post(self):
        me.bank = self.request.get('bank')
        self.redirect('/bank2')

# stores most of the user's data
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
        me.company = self.request.get('company')

        self.redirect('/login') #TAKE THEM TO THE NEXT PAGE HERE


class UploadCertificate(webapp2.RequestHandler):
    def post(self):
        self.redirect('/certificate-form')


class CertificateForm(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENVIRONMENT.get_template('certificateform.html')
        self.response.write(template.render({"user": me}))

class CertificateStore(webapp2.RequestHandler):
    def post(self):
        me.name = self.request.get('name')
        me.address = self.request.get('address')
        me.city = self.request.get('city')
        me.state = self.request.get('state')
        me.country = self.request.get('country')
        me.zip = self.request.get('zip')
        me.sex = self.request.get('sex')
        me.ssn = self.request.get('ssn')
        me.age_at_death = self.request.get('age_at_death')
        me.date_of_birth = self.request.get('date_of_birth')
        me.date_of_death = self.request.get('date_of_death')
        me.birthplace = self.request.get('birthplace')
        me.resident_state = self.request.get('resident_state')
        me.resident_county = self.request.get('resident_county')
        me.resident_town = self.request.get('resident_town')
        me.resident_address = self.request.get('resident_address')
        me.resident_apptnum = self.request.get('resident_apptnum')
        me.resident_zip = self.request.get('resident_zip')
        me.us_armed_forces = self.request.get('us_armed_forces')
        me.fathers_name = self.request.get('fathers_name')
        me.mothers_name = self.request.get('mothers_name')
        me.surviving_spouse_name = self.request.get('surviving_spouse_name')
        me.marital_status = self.request.get('marital_status')
        me.your_name = self.request.get('your_name')
        me.your_relationship = self.request.get('your_relationship')
        me.your_address = self.request.get('your_address')

        self.redirect('/')

application = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/cert', MainPage2),
    ('/login', LoginPage),
    ('/certificate', CertificatePage),
    ('/funeral', FuneralPage),
    ('/social', SocialPage),
    ('/finance', FinancePage),
    ('/memberships', MembershipPage),
    ('/store', Store), # doesnt do anything just captures post
    ('/storeBank', StoreBank), # doesnt do anything just captures post
    ('/bank2', FinancePage2),
    ('/certificate-upload', UploadCertificate),
    ('/certificate-form', CertificateForm),
    ('/certificate-store', CertificateStore)
], debug=True)
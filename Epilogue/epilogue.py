import os, lob
import urllib, cgi
import time
import jinja2
import webapp2
from google.appengine.api import users
import FormFiller
import stripe
stripe.api_key = "sk_test_4W9L9sr4pWYjeOpTkPDPtugi"
lob.api_key = 'test_3aa918f64396a4f31c68c80f3238a617d8f'
from models import User
me = User()
status = 0
myAddress = {}

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

class ResetPage(webapp2.RequestHandler):
    def get(self):
        me = User()
        self.response.write("Reset")

# THIS ENTIRE CLASS IS DEPRECATED
class MainPage(webapp2.RequestHandler):
    def get(self):
        return self.redirect('/')
#        user = users.get_current_user()
#        if user:  # signed in already
#            #self.response.out.write('Hello <em>%s</em>! [<a href="%s">sign out</a>]' % (
#            #    user.nickname(), users.create_logout_url(self.request.uri)))
#            self.redirect('/cert')
#        else:     # let user choose authenticator
#            self.response.out.write('Hello world! Sign in at: ')
#            for name, uri in providers.items():
#                self.response.out.write('[<a href="%s">%s</a>]' % (
#                    users.create_login_url(federated_identity=uri), name))

class MainPage2(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if not user:
            self.redirect(users.create_login_url(users.create_login_url(self.request.uri)))
        if me.did_deathcertificate:
            self.redirect("/certificate-form")
        template = JINJA_ENVIRONMENT.get_template('frontpage.html')
        self.response.write(template.render({'message': "index"}))


class CertificatePage(webapp2.RequestHandler):
    def get(self):
        if me.did_deathcertificate:
            self.redirect("/")
        template = JINJA_ENVIRONMENT.get_template('certificate.html')
        self.response.write(template.render({'message': "Certificate",
                                             'color': 'yellow'}))

class CertificateEnter(webapp2.RequestHandler):
    def get(self):
        me.name = "Jessie Kris Lambert"
        me.address = "851 Church Street"
        me.city = "Mountain View"
        me.state = "California"
        me.country = ""
        me.zip = "94041"
        me.sex = "Male"
        me.ssn = "123-456-7890"
        me.age_at_death = "62"
        me.date_of_birth = "08/02/2014"
        me.date_of_death = ""
        me.birthplace = "Wichita, KS"
        me.resident_state = "California"
        me.resident_county = "Santa Clara County"
        me.resident_town = "Mountain View"
        me.resident_address = "851 Church Street"
        me.resident_apptnum = "1227"
        me.resident_zip = "94041"
        me.us_armed_forces = "Yes"
        me.fathers_name = "Jackson Bill Lambert"
        me.mothers_name = "Katarina Lee"
        me.surviving_spouse_name = "Jennifer Menendez"
        me.marital_status = "Married"
        me.your_name = "Stephen Lambert"
        me.your_relationship = "Son"
        me.your_address = "1532 Willows Way, Los Altos, CA 94024"
        time.sleep(7)
        self.redirect('/certificate-form')

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
        elif me.company is 'Google':
            yourAddress = lob.Address.create(
                name='Google, Gmail User Support - Decedents Accounts',
                address_line1='1600 Amphitheatre Parkway',
                address_city='Mountain View',
                address_state='CA',
                address_country='US',
                address_zip='94043'
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
        template = JINJA_ENVIRONMENT.get_template('funeral.html')
        self.response.write(template.render(
            {'message': "Arrange Funeral Services",
             'user': me,
             'color': 'pink'}))


class SocialPage(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENVIRONMENT.get_template('social.html')
        params = {
            'message': "Social Media Cancellation",
            'user': me,
            'sent': self.request.get('sent', ""),
            'color': 'gold'
        }
        self.response.write(template.render(params))


class FinancePage(webapp2.RequestHandler):
    def get(self):
        params = {
            'sent': self.request.get('submit', ""),
            'message': "Finance",
            'color': 'orange',
            'page_num': 1,
            'job_id': self.request.get('job', "")
        }

        template = JINJA_ENVIRONMENT.get_template('finance.html')
        self.response.write(template.render(params))

class FinancePage2(webapp2.RequestHandler):
    def get(self):
        self.response.write('Call THIS NUMBER to cancel with ' + me.bank)
        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render({'message': "finance",
                                             "bank": me.bank,
                                             'color': 'orange'}))
        # to do later: use the bank in the actual html

class MembershipPage(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENVIRONMENT.get_template('memberships.html')
        self.response.write(template.render({'message': "Manage Benefits",
                                             'color': 'red'}))

#stores which banks the user uses
class StoreBank(webapp2.RequestHandler):
    def get(self):
        me.bank = self.request.get('bank')
        yourAddress = {}
        if me.bank == 'Chase':
            yourAddress = lob.Address.create(
                name='National Bank By Mail',
                address_line1='1600 Amphitheatre Parkway',
                address_city='Louisville',
                address_state='KY',
                address_country='US',
                address_zip='40233')
        elif me.bank == 'Bank of America':
            yourAddress = lob.Address.create(
                name='Bank of America',
                address_line1='Suite 6001 P.O. Box 803126',
                address_city='Dallas',
                address_state='TX',
                address_country='US',
                address_zip='75380')

        myAddress = lob.Address.create(
            name='test',
            address_line1=me.resident_address,
            address_city=me.resident_town,
            address_state='CA',
            address_country='US',
            address_zip=me.resident_zip
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

        self.redirect('/finance?submit=true&job=' + job["id"] )

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
        print me.name
        print me.address
        print "^INFOOOOO"
        template = JINJA_ENVIRONMENT.get_template('certificateform.html')
        self.response.write(template.render({"user": me,
                                             'color': 'yellow'}))

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

        if me.did_deathcertificate:
            self.redirect('/next?certificate=edit');
        else:
            me.did_deathcertificate = True
            self.redirect('/next?certificate=new');



class GooglePage(webapp2.RequestHandler):
    def get(self):
        me.did_google = True

        myAddress = lob.Address.create(
            name='test',
            address_line1=me.resident_address,
            address_city=me.resident_town,
            address_state='CA',
            address_country='US',
            address_zip=me.resident_zip
        )

        yourAddress = lob.Address.create(
            name='Google, Gmail User Support - Decedents Accounts',
            address_line1='1600 Amphitheatre Parkway',
            address_city='Mountain View',
            address_state='CA',
            address_country='US',
            address_zip='94043'
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

        self.redirect('/social?sent=google')

class DropBoxPage(webapp2.RequestHandler):
    def get(self):
        myAddress = lob.Address.create(
            name='test',
            address_line1=me.resident_address,
            address_city=me.resident_town,
            address_state='CA',
            address_country='US',
            address_zip=me.resident_zip
        )

        yourAddress = lob.Address.create(
            name='Dropbox Legal Department Decedents Accounts',
            address_line1='185 Berry St. Suite 400',
            address_city='San Francisco',
            address_state='CA',
            address_country='US',
            address_zip='94107'
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

        me.did_dropbox = True
        self.redirect('/social?sent=dropbox')

class DidSocial(webapp2.RequestHandler):
    def post(self):
        name = self.request.get('name')
        if name == "fb":
            me.did_fb = True
        elif name == "linkedin":
            me.did_linkedin = True
        elif name == "emailoptout":
            me.did_email = True
        elif name == "addresschange":
            me.did_postoffice = True
        elif name == "donotcontact":
            me.did_phone = True
        self.redirect('/social')

class NextPage(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENVIRONMENT.get_template('next.html')
        params = {'message': "certificate",
                  'certificate': self.request.get('certificate', "")}
        self.response.write(template.render(params))

class StripeTest(webapp2.RequestHandler):
    def get(self):
        stripebutton = """<form action="" method="POST">
  <script
    src="https://checkout.stripe.com/checkout.js" class="stripe-button"
    data-key="pk_test_4W9LvKOHPuWXpO5h8z7v6q7D"
    data-amount="2000"
    data-name="Epilogue"
    data-description="Print & Mail Service, Dropbox ($2.00)"
    data-image="stylesheets/img/stripelogo.png">
  </script>
</form>"""
        html = """<html><body>%s</body></head>""" % stripebutton
        self.response.write(html)

    def post(self):
        token = self.request.get('stripeToken')
        try:
            charge = stripe.Charge.create(
                amount=1000, # amount in cents, again
                currency="usd",
                card=token,
                description="payinguser@example.com"
                )
            self.response.write(charge)
        except stripe.CardError, e:
            # The card has been declined
            pass




application = webapp2.WSGIApplication([
    ('/cert', MainPage), #<-- deprecated, ask Pranav
    ('/', MainPage2),
    ('/login', LoginPage),
    ('/certificate', CertificatePage),
    ('/funeral', FuneralPage),
    ('/social', SocialPage),
    ('/finance', FinancePage),
    ('/next', NextPage),
    ('/memberships', MembershipPage),
    ('/store', Store), # doesnt do anything just captures post
    ('/storeBank', StoreBank), # doesnt do anything just captures post
    ('/bank2', FinancePage2),
    ('/certificate-upload', UploadCertificate),
    ('/certificate-form', CertificateForm),
    ('/certificate-store', CertificateStore),
    ('/certificate-enter', CertificateEnter),
    ('/did-social', DidSocial),
    ('/fb', FormFiller.FBPage),
    ('/linkedin', FormFiller.LinkedInPage),
    ('/emailoptout', FormFiller.EmailOptOutPage),
    ('/addresschange', FormFiller.AddressChangePage),
    ('/donotcontact', FormFiller.DoNotContactPage),
    ('/google', GooglePage),
    ('/dropbox', DropBoxPage),
    ('/stripetest', StripeTest),
    ('/reset', ResetPage)
], debug=True)

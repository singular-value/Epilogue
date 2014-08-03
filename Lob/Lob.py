import webapp2
import lob

lob.api_key = 'test_3aa918f64396a4f31c68c80f3238a617d8f'

class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write('Hello, World!')

        # user's own address
        myAddress = lob.Address.create(
            name='Joe Smith',
            address_line1='104, Printing Boulevard',
            address_city='Boston',
            address_state='MA',
            address_country='US',
            address_zip='12345'
        )

        # address of people to send
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
            file=open('Letter.pdf','rb'), # change to death cert image
            setting_id='100', # change to 500
            quantity=1
        )

        job = lob.Job.create(
            name='Joe First Job',
            to_address=yourAddress,
            from_address=myAddress,
            objects = [certificate,letter]
        )

        self.response.write(job)


application = webapp2.WSGIApplication([
    ('/', MainPage),
], debug=True)
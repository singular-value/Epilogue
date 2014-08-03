"""Contains a generic fillForm method, which fills out a form based on
the POST url and form_fields (a dictionary). MainPage does an example
of searching HUGO BOSS for 'jeans'. To run it, add this directory to
GAE and run it."""

import webapp2
import urllib

from google.appengine.api import urlfetch

def fillForm(url, form_fields):
    form_data = urllib.urlencode(form_fields)
    result = urlfetch.fetch(url=url, payload=form_data, method=urlfetch.POST)
    return result

class MainPage(webapp2.RequestHandler):
    def get(self):
        form_fields = {
            "searchValue": "jeans"
            }
        url = "http://www.hugoboss.com/uk/en/searchresult.php"
        result = fillForm(url, form_fields).content
        result = result.replace("<head>", """<head><base href="%s">""" % url)
        self.response.write(result)

#class OtherPage(webapp2.RequestHandler):
#    def get(self):
#        htmlcode = 

application = webapp2.WSGIApplication([
    ('/', MainPage),
], debug=True)

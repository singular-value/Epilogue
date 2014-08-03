"""Contains a generic fillForm method, which fills out a form based on
the POST url and form_fields (a dictionary). MainPage does an example
of searching HUGO BOSS for 'jeans'. To run it, add this directory to
GAE and run it."""

import webapp2
import urllib

from google.appengine.api import urlfetch

head = """<html><head>
<style>
#iframe-form {
position:fixed;
right: 0;
top: 45%;
}
.btn-label {
font-family: 'Open Sans', sans-serif;
font-size: 25px;
font-weight: 700;
color: #555;
position: absolute;
top: 30px;
right: 130px;
}
.btn-primary {
background-image: url('stylesheets/img/chevron-grey.png');
background-repeat: no-repeat;
background-color: transparent;
border:none;
height:100px;
width:100px;
outline:none;
-webkit-transition: all 300ms;
transition: all 300ms;
}
#iframe-form .btn-primary:hover {
background-image: url('stylesheets/img/chevron.png');
}
</style><script>"""
tail = """</script>
</head>
<body><iframe id="the_form" width="1000px" height="800px" src="%s" onload="fill()"></iframe>
<form id="iframe-form" method="post" action="/did-social">
  <input type="hidden" name="name" value="%s" />
  <div class="btn-label">CONTINUE</div>
  <input type="submit" class="btn btn-primary" value="">
</form>
</body></html>"""

def fillForm(url, form_fields):
    form_data = urllib.urlencode(form_fields)
    result = urlfetch.fetch(url=url, payload=form_data, method=urlfetch.POST)
    return result

class DoNotContactPage(webapp2.RequestHandler):
    def get(self):
        url = "forms/donotcontact.htm"
        self.response.write(head +
"""fill = function() {
var iframe = document.getElementById('the_form');
var innerDoc = iframe.contentDocument || iframe.contentWindow.document;
form = innerDoc.forms[0]
form["member.firstName"].value = "%s"
form["member.middleName"].value = "%s"
form["member.lastName"].value = "%s"
form["addressList.address1[0]"].value = "%s"
form["addressList.city[0]"].value = "%s"
form["addressList.state[0]"].value = "%s"
form["addressList.zipCode[0]"].value = "%s"
form["month"].value = "%s"
form["year"].value = "%s"
form["age"].value = "%s"
form["member.fnamesub"].value = "%s"
form["member.lnamesub"].value = "%s"
form["relate"].value = "%s"
form["member.email"].value = "%s"
form["confirmEmail"].value = "%s"
}""" % ("Jessie", "K", "Lambert", "851 Church Street", "Mountain View", "CA", "94041", "08", "2014", "62", "Stephen", "Lambert", "Son", "epilogueemail@epilog.ue", "epilogueemail@epilog.ue")
+ tail % (url, "donotcontact"))


class EmailOptOutPage(webapp2.RequestHandler):
    def get(self):
        url = "forms/emailoptout.htm"
        self.response.write(head + """
fill = function() {
var iframe = document.getElementById('the_form');
var innerDoc = iframe.contentDocument || iframe.contentWindow.document;
form = innerDoc.forms[0]
form["email1"].value = "%s"
}""" % ("epiloguesemail@pilog.ue") + tail % (url, "emailoptout"))


class AddressChangePage(webapp2.RequestHandler):
    def get(self):
        url = "forms/addresschange.htm"
        self.response.write(head + """
fill = function() {
var iframe = document.getElementById('the_form');
var innerDoc = iframe.contentDocument || iframe.contentWindow.document;
form = innerDoc.forms[0]
form["startDateStr"].value = "%s"
form["mover.person.firstName"].value = "%s"
}""" % ("08/04/2014","Testing") + tail % (url, "addresschange"))


class LinkedInPage(webapp2.RequestHandler):
    def get(self):
        url = "forms/linkedin.htm"
        self.response.write(head + """
fill = function() {
var iframe = document.getElementById('the_form');
var innerDoc = iframe.contentDocument || iframe.contentWindow.document;
form = innerDoc.forms[0]
form["ds$hldrBdy$Member_UserName"].value="%s"
form["ds$hldrBdy$Member_Email"].value="%s"
}""" % ("Stephen Lambert", "epiloguesemail@pilog.ue") + tail % (url, "linkedin"))


class FBPage(webapp2.RequestHandler):
    def get(self):
        url="forms/fb.htm"
        self.response.write(head + """
fill = function() {
var iframe = document.getElementById('the_form');
var innerDoc = iframe.contentDocument || iframe.contentWindow.document;
form = innerDoc.forms[1]
form["Field153786764731152"].value="%s"
form["Field131943620266906"].value="%s"
form["Field300731829979004"].value="%s"
form["Field152395278213769"].value="%s"
form["Field243993725684212"].value="%s"
form["Field229650377126227"].value="%s"
}""" % ("Jessie Kris Lambert","https://www.facebook.com/bob.cardinal.50","bob.cardinal.epiloguetesting@gmail.com","epiloguesemail@pilog.ue","Immediate family ","Memorialize")
         + tail % (url, "fb"))
#        url = "https://www.facebook.com/help/contact/305593649477238"
#        result = urlfetch.fetch(url=url, method=urlfetch.GET)
#        print result.content
#        self.response.headers['Content-Type'] = 'text/plain'
#        self.response.write(result.content.replace("<head>", """<head><base href="%s">""" % url))

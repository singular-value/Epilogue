from webapp2_extras.appengine.auth.models import User
from google.appengine.ext import ndb


class User(User):
    """
    Universal user model. Can be used with App Engine's default users API,
    own auth or third party authentication methods (OpenID, OAuth etc).
    """
    #: Creation date.
    created = ndb.DateTimeProperty(auto_now_add=True)
    #: Modification date.
    updated = ndb.DateTimeProperty(auto_now=True)
    #: User defined unique name, also used as key_name.
    # Not used by OpenID
    username = ndb.StringProperty()
    #: User Name
    name = ndb.StringProperty()
    #: User email
    email = ndb.StringProperty()
    #: Hashed password. Only set for own authentication.
    # Not required because third party authentication
    # doesn't use password.
    password = ndb.StringProperty()
    #: User Country
    country = ndb.StringProperty()
    #: User TimeZone
    tz = ndb.StringProperty()
    #: Account activation verifies email
    activated = ndb.BooleanProperty(default=False)
    #: helper property to get the users full name
    full_name = ndb.ComputedProperty(lambda self: self.name + " " + self.last_name)

    dead_name = ndb.StringProperty()

    address= ndb.StringProperty()
    city= ndb.StringProperty()
    state= ndb.StringProperty()
    country= ndb.StringProperty()
    zip= ndb.StringProperty()
    sex = ndb.StringProperty()
    ssn = ndb.StringProperty()
    age_at_death = ndb.StringProperty()
    date_of_birth = ndb.StringProperty()
    date_of_death = ndb.StringProperty()
    birthplace = ndb.StringProperty()
    resident_state = ndb.StringProperty()
    resident_county = ndb.StringProperty()
    resident_town = ndb.StringProperty()
    resident_address = ndb.StringProperty()
    resident_apptnum = ndb.StringProperty()
    resident_zip = ndb.StringProperty()
    us_armed_forces = ndb.StringProperty()
    fathers_name = ndb.StringProperty()
    mothers_name = ndb.StringProperty()
    surviving_spouse_name = ndb.StringProperty()
    marital_status = ndb.StringProperty()
    your_name = ndb.StringProperty()
    your_relationship = ndb.StringProperty()
    your_address = ndb.StringProperty()

    company = ndb.StringProperty()

    did_fb = ndb.BooleanProperty(default = False)
    did_linkedin = ndb.BooleanProperty(default = False)
    did_email = ndb.BooleanProperty(default = False)
    did_phone = ndb.BooleanProperty(default = False)
    did_postoffice = ndb.BooleanProperty(default = False)
    did_deathcertificate = ndb.BooleanProperty(default = False)
    did_dropbox = ndb.BooleanProperty(default = False)
    did_google = ndb.BooleanProperty(default = False)
    did_twitter = ndb.BooleanProperty(default = False)
    did_paypal = ndb.BooleanProperty(default = False)


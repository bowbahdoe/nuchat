# REMEMBER TO CHANGE THE DEBUG FLAG
# DURING PRODUCTION
DEBUG = True

# Used for WTForms
WTF_CSRF_ENABLED = False
SECRET_KEY = 'eshwre98fhw98r4'

ALLOW_CORS = True

# and mongoengine
MONGODB_SETTINGS = {
    'db': 'nuchat',
    'host': 'dsXXXXXX.mlab.com',
    'port': 37197,
    'username': 'usename',
    'password': 'password'
}

# Flask-Security config
SECURITY_REGISTERABLE = True
#SECURITY_RECOVERABLE  = False
SECURITY_CHANGEABLE   = True
SECURITY_URL_PREFIX   = '/security'
SECURITY_PASSWORD_HASH = 'sha512_crypt'
SECURITY_TOKEN_MAX_AGE	= 3601
SECURITY_PASSWORD_SALT = "ASFJsefnsejfsefnjcEfnhi4rw3rt43t"

SECURITY_USER_IDENTITY_ATTRIBUTES = ('username','email')

import warnings
import flask
from flask import Flask, session, send_from_directory 
from flask_security import Security, MongoEngineUserDatastore
import flask_security.forms as fsf
from flask_security.decorators import login_required
from flask_login import current_user
from flask_socketio import SocketIO
from flask_cors import CORS
from flask.exthook import ExtDeprecationWarning
with warnings.catch_warnings():
    warnings.simplefilter('ignore', ExtDeprecationWarning)
    from flask_mongoengine import MongoEngine


    
###########################################################
# The main app instance                                   #
#                                                         #
# This is passed around the application to handle routing #
###########################################################
app = Flask(__name__)



############################################################
# Load in configuration instead of defining explicitly     #
# within this file. consult the file if a change is needed #
############################################################
app.config.from_pyfile('config.py')

###############################################################
# Sets the variable db to represent our connection to MongoDB #
# This is needed by blueprints that want to define their own  #
# models                                                      #
###############################################################
db = MongoEngine(app)

if app.config['ALLOW_CORS']:
    CORS(app)
###############################################################
# sets up the Flask-Security Instance using the User and Role #
# models defined in mrmccue.models                            #
###############################################################

from nuchat.models import User, Role

class ExtendedRegisterForm(fsf.RegisterForm):
    first_name = fsf.StringField('First Name', [fsf.Required()])
    last_name = fsf.StringField('Last Name', [fsf.Required()])
    username = fsf.StringField('Username', [fsf.Required()])

user_datastore = MongoEngineUserDatastore(db, User, Role)
security = Security(app, user_datastore,register_form=ExtendedRegisterForm)

socketio = SocketIO(app)

#socketio.init_app(app)

import nuchat.views

@app.route('/')
def index():
    return send_from_directory('static','index.html')
    
    
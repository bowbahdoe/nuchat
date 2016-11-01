import functools
import flask
import typing as t
from nuchat import socketio
from nuchat import app
from flask_socketio import emit, disconnect
from flask_login import current_user
from flask import jsonify
from nuchat import models

ONLINE_USERS = set()

Number = t.Union[int, float]
# -------------------------------------------- #
# This JSON definition ignores nested objects, #
# but it works for general cases               #
# -------------------------------------------- #
JSON = t.Union[str,
               Number,
               bool,
               None,
               t.List[t.Union[str, Number]],
               t.Dict[str, t.Union[str, Number]]]

def authenticated_only(f):
    '''
    wrapper for a socket connection.
    disconnects users with no authentication
    '''
    @functools.wraps(f)
    def wrapped(*args, **kwargs):
        if not current_user.is_authenticated:
            disconnect()
        else:
            return f(*args, **kwargs)
    return wrapped

@socketio.on('user message')
def handle_message(msg: JSON) -> None:
    '''
    msg is a JSON which has the following properties
    {'sender_username': ...,
     'recipients': [str]
     'content_type': ['text' or 'image_url']
     'content': ...}
    '''
    if not is_valid_user_message(msg):
        return

    if current_user.is_authenticated:
        emit('server message',
             '%s: %s' % (current_user.email, msg['content']),
             broadcast=True)
    else:
        emit('server message','Annonymous: %s' % msg['content'], broadcast=True)
        
def is_valid_user_message(msg: JSON) -> bool:
    '''
    returns whether a given JSON message conforms to a user_message
    '''

    try:
        assert type(msg) == dict
        assert ('sender_username' in msg and
                'recipients'      in msg and 
                'content_type'    in msg and
                'content'         in msg)
        assert type(msg['sender_username']) == str
        assert type(msg['recipients']) == list
        assert all((type(name) == str for name in msg['recipients']))
        assert len(msg['recipients']) > 0
        assert msg['content_type'] in ('text', 'image')
        assert type(msg['content']) == str

    except AssertionError:
        return False
        
    return True


@socketio.on('connect')
def handle_connect(*msg):
    if current_user.is_authenticated:
        ONLINE_USERS.add(current_user.email)

@socketio.on('disconnect')
def handle_disconnect(*msg):
    if current_user.is_authenticated:
        ONLINE_USERS.discard(current_user.email)


@app.route('/get_online_users')
def get_online_users() -> flask.wrappers.Response:
    '''
    returns as JSON to an authenticated user the list of their
    friends who are currently online
    
    if the user is unauthenticated, returns an empty
    list as JSON
    '''
    if current_user.is_authenticated:
        are_we_friends = functools.partial(are_friends, current_user.email)
        return jsonify(list(filter(are_we_friends, ONLINE_USERS)))
    else:
        return jsonify([])

def are_friends(user_1: str, user_2: str) -> bool:
    '''
    STUB. returns whether two users are friends
    '''
    return True


@app.route('/messages', methods=['GET'])
@app.route('/messages/<int:n>', methods=['GET'])
def fetch_messages(n=1):
    if current_user.is_authenticated:
        pass

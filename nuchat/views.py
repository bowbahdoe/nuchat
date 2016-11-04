import functools
import flask
import typing as t
import mongoengine as mongo
import flask_wtf as wtf
import nuchat.models as m
from nuchat.friends import are_friends, process_friend_request,\
                           get_friends, does_user_exist
from nuchat import socketio
from nuchat import app
from flask_socketio import emit, disconnect
from flask_login import current_user, login_required
from flask import jsonify

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
    {'sender_username': str,
     'recipients': [str...]
     'content_type': ['text' or 'image_url']
     'content': str}
    '''
    if not is_valid_user_message(msg):
        return

    if current_user.is_authenticated:
        emit('server message',
             '%s: %s' % (current_user.username, msg['content']),
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
        ONLINE_USERS.add(current_user.username)

@socketio.on('disconnect')
def handle_disconnect(*msg):
    if current_user.is_authenticated:
        ONLINE_USERS.discard(current_user.username)


@app.route('/get_online_users', methods=['GET'])
def get_online_users() -> flask.wrappers.Response:
    '''
    returns as JSON to an authenticated user the list of their
    friends who are currently online
    
    if the user is unauthenticated, returns an empty
    list as JSON
    '''
    if current_user.is_authenticated:
        are_we_friends = functools.partial(are_friends, current_user.username)
        return jsonify(list(filter(are_we_friends, ONLINE_USERS)))
    else:
        return jsonify([])

@app.route('/is_logged_in', methods=['GET'])
def is_logged_in() -> flask.wrappers.Response:
    '''
    returns whether the user requesting has login credentials
    
    useful for when credentials expire
    '''
    return jsonify(current_user.is_authenticated)

@app.route('/submit_friend_request/', methods=['POST'])
@login_required
def submit_friend_request():
    '''
    submits a friend request from one user to another
    
    if the other user sends the same request,
    the request is formalized
    '''
    
    if 'username' not in request.form:
        return
    
    username = request.form['username']
    
    if username == current_user.username:
        return

    process_friend_request(sender=current_user.username,
                           reciever=username)

@app.route('/get_friends/', methods=['GET'])
@app.route('/get_friends/<username>', methods=['GET'])
@login_required
def get_my_friends(username=None):
    '''
    If a user is provided, gets the friends of that user if
    you are friends with that user.
    
    If no user provided, defaults to getting the friends
    of the user who made the request
    '''
    if not username:
        username = current_user.username
    
    if not does_user_exist(username) or \
       not are_friends(username, current_user.username):
        response = {'error': 'the requested user\'s friends are not available'}
        
        return jsonify(response), 404
    else:
        response = {'username': username,
                    'friends': get_friends(username)}
    
        return jsonify(response)

@app.route('/messages', methods=['GET'])
@app.route('/messages/<int:n>', methods=['GET'])
def fetch_messages(n=1):
    if current_user.is_authenticated:
        pass

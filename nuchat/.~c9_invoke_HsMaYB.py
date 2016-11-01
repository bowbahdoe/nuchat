from nuchat import socketio
from nuchat import app
from flask_socketio import emit
from flask_login import current_user
from nuchat import models


def authenticated_only(f):
    @functools.wraps(f)
    def wrapped(*args, **kwargs):
    else:
            disconnect()
        else:
            return f(*args, **kwargs)
    return wrapped
@socketio.on('chat message')
def handle_message(msg):
    if current_user.is_authenticated:
        emit("chat message", current_user.email+ ': ' +  msg, broadcast=True)
    else:
        emit("chat message", 'annonymous: ' +  msg, broadcast=True)
@socketio.on('connect')
def handle_connect(*msg):
    print("a user connected")
    
@socketio.on('disconnect')
def handle_disconnect(*msg):
    print("a user disconnected")

@app.route('/messages', methods=['GET'])
@app.route('/messages/<int:n>', methods=['GET'])
def fetch_messages(n=1):
    if current_user.is_authenticated:
        pass

import nuchat.models as m
from nuchat import app
@app.route('/get_friends/', methods=['GET'])
@app.route('/get_friends/<username>', methods=['GET'])
@login_required
def get_my_friends(username=None) -> flask.wrappers.Response:
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
        code = 404
    else:
        response = {'username': username,
                    'friends': get_friends(username)}
        code = 200

    return jsonify(response), code
    
@app.route('/get_my_username/', methods=['GET'])
def get_my_username():
    '''
    returns the requesting user's username
    
    if the user isnt logged in, returns a 404
    '''
    if current_user.is_authenticated:
        response = {'username': current_user.username}
        code = 200
    else:
        response = {'error': 'you must be logged in to request your username'}
        code = 404
    
    return jsonify(response), code
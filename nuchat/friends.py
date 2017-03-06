'''
Module for handling logic associated with friend requests
'''
import nuchat.models as m

def process_friend_request(*,sender, reciever) -> None:
    '''
    submits a friend request from one user to another
    
    if the other user sends the same request,
    the request is formalized
    '''

    if does_user_exist(reciever) and not are_friends(reciever, sender):
        if has_user_requested_friendship(reciever, sender):
            make_friends(reciever, sender)
            m.FriendRequestCollection.delete_many(
                {'sender': sender, 'reciever': reciever})
            m.FriendRequestCollection.delete_many(
                {'sender': reciever, 'reciever': sender})
        else:
            if not m.FriendRequestCollection.find({'sender':sender,
                                                   'reciever': reciever}).count():
                m.FriendRequest(sender=sender,
                                reciever=reciever).save()

def does_user_exist(username):
    '''
    returns whether a given user can be found in the
    database
    '''

    return bool(m.UserCollection.find({'username': username}).count())

def are_friends(user_1: str, user_2: str) -> bool:
    '''
    returns whether two users are friends.
    raises a lookup error if one does not exist
    '''
    if user_1 == user_2:
        return True

    if not does_user_exist(username):
        raise LookupError('user not found')

    else:
        f_1 = m.UserCollection.find_one({'username': user_1})['friends']
        f_2 = m.UserCollection.find_one({'username': user_2})['friends']

        return user_1 in f_2 and user_2 in f_1

def has_user_requested_friendship(requester: str, requestee: str) -> bool:
    '''
    returns whether a given user has sent a friend request to the other user
    '''

    return bool(m.FriendRequestCollection.find({'sender': requester,
                                                'reciever': requestee}).count())
def get_friends(username: str):
    '''
    returns the friends of the passed user
    
    raises a lookup error if the user does not exist
    '''
    if not does_user_exist(username):
        raise LookupError('user not found')
    
    return m.UserCollection.find_one({'username': username})['friends']
    
    
def make_friends(user_1, user_2):
    '''
    sets the two users to be friends;
    assumes both exist
    '''
    first = m.User.objects.get(username=user_1)
    second = m.User.objects.get(username=user_2)
    
    first.friends.append(user_2)
    first.friends = list(set(first.friends))
    second.friends.append(user_1)
    second.friends = list(set(second.friends))
    
    first.save()
    second.save()
from nuchat import db
from flask_security import UserMixin, RoleMixin

class Role(db.Document, RoleMixin):
    '''
    Stores the role of a user
    '''
    name = db.StringField(max_length=80, unique=True)
    description = db.StringField(max_length=255)

RoleCollection = Role._get_collection()

class User(db.Document, UserMixin):
    '''
    represents a user in the system
    '''
    email = db.StringField(max_length=255, unique=True)
    first_name = db.StringField(max_length=255)
    last_name = db.StringField(max_length=255)
    username = db.StringField(max_length=255, unique=True)
    password = db.StringField(max_length=255)
    friends = db.ListField(db.StringField(max_length=255))
    active = db.BooleanField(default=True)
    confirmed_at = db.DateTimeField()
    roles = db.ListField(db.ReferenceField(Role), default=[])

UserCollection = User._get_collection() 

class Message(db.Document):
    '''
    Represents a single message sent from one user to another
    '''
    sender = db.ReferenceField(User, required=True)
    recipient = db.ListField(db.ReferenceField(User), required=True)
    time_sent = db.DateTimeField(required=True)
    contents = db.StringField(required=True)

MessageCollection = Message._get_collection()

class MessageThread(db.Document):
    participants = db.ListField(db.ReferenceField(User), required=True)
    messages = db.ListField(db.ReferenceField(Message))

MessageThreadCollection = MessageThread._get_collection()

class FriendRequest(db.Document):
    sender = db.ReferenceField(User, required=True)
    reciever = db.ReferenceField(User, required=True)

FriendRequestCollection = FriendRequest._get_collection()
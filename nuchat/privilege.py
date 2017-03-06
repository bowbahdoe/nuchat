from nuchat import app
import nuchat.models as m

@app.before_first_request
def create_admin_role():
    '''
    creates the admin role if one doesnt already exist
    '''
    if m.RoleCollection.find_one({'name': 'admin'}) == None:
        m.Role(name="admin",
               description="admin of the site. power over all").save()
    
def make_admin(username):
    pass
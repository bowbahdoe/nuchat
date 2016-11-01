import nuchat.views as v

def test_user_message_check():
    '''
    tests the check on user messages
    '''
    # Make sure the function returns the right type
    assert type(v.is_valid_user_message(1)) == bool
    
    # correctly structured messages
    assert v.is_valid_user_message({'sender_username': 'name',
                                    'recipients': ['person_1', 'person_2'],
                                    'content_type': 'text',
                                    'content': 'this-is-my-message'})
                                    
    assert v.is_valid_user_message({'sender_username': 'name',
                                    'recipients': ['person_1', 'person_2'],
                                    'content_type': 'image',
                                    'content': 'this-is-my-message'})
    
    # Technically valid JSON, but make no sense in context                        
    assert not v.is_valid_user_message('hi')
    assert not v.is_valid_user_message(None)
    assert not v.is_valid_user_message(False)
    assert not v.is_valid_user_message(True)
    assert not v.is_valid_user_message(3)
    
    # Dictionary without the correct values
    assert not v.is_valid_user_message({'data': 'values'})
    
    # Invalid username
    assert not v.is_valid_user_message({'sender_username': 2,
                                        'recipients': ['person_1', 'person_2'],
                                        'content_type': 'text',
                                        'content': 'this-is-my-message'})
    
    # Examples of invalid recipients
    assert not v.is_valid_user_message({'sender_username': 'name',
                                        'recipients': [],
                                        'content_type': 'text',
                                        'content': 'this-is-my-message'})
    assert not v.is_valid_user_message({'sender_username': 'name',
                                        'recipients': [1],
                                        'content_type': 'text',
                                        'content': 'this-is-my-message'})
    assert not v.is_valid_user_message({'sender_username': 'name',
                                        'recipients': 'invalid recipients',
                                        'content_type': 'text',
                                        'content': 'this-is-my-message'})

    # Examples of invalid content
    assert not v.is_valid_user_message({'sender_username': 'name',
                                        'recipients': ['person_1', 'person_2'],
                                        'content_type': 'foomble',
                                        'content': 'this-is-my-message'})

    assert not v.is_valid_user_message({'sender_username': 'name',
                                        'recipients': ['person_1', 'person_2'],
                                        'content_type': 'text',
                                        'content': {'I have sent the wrong data!': 'hahahaha'}})
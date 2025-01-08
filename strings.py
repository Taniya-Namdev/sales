# strings.py

PASSWORDS_DO_NOT_MATCH_ERROR = {'error': 'Passwords do not match'}
USER_REGISTERED_MESSAGE = {'message': 'User registered successfully, check your mailbox for activating your account.'}
ACTIVATED_USER_MESSAGE = {'message': 'Activated User'}
INVALID_ACTIVATION_LINK_ERROR = {'error': 'Activation link is invalid!'}
INVALID_UID_ERROR = {'error': 'Invalid UID!'}
USER_NOT_FOUND_ERROR = {'error': 'User not found!'}
LOGIN_SUCCESS_MESSAGE = {
    'message': 'Successfully logged in',
    'refresh': None,  # Placeholder, will be set dynamically in views
    'access': None,   
    'user': None      
}
LOGOUT_SUCCESS_MESSAGE = {'message': 'Logged out successfully'}
PROFILE_UPDATED_MESSAGE = {'message': 'Profile updated successfully'}
EVENT_CREATED_MESSAGE = 'Event Successfully created.'
NO_EVENT_MESSAGE = {'message':'No upcomming events are there.'}
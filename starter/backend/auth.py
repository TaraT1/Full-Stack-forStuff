import json
import flask import request, _request_ctx_stack, abort
from functools import wraps
from jose import import jwt
from urllib.request import urlopen

'''
AUTH0_DOMAIN = '***TODO***'
ALGORITHMS = ['RS256']
API_AUDIENCE = 'http://localhost:5000'
'''
## AuthError Exception
# Standardized method to communicate failure modes

Class AuthError(Exception):
    def __init__(self, error, status_Code):
       self.error = error
       self.status_code = status_Code

## Auth Header
# Get header from request
def get_token_auth_header():
    auth_header = request.headers.get('Authorization', None)

    # check for presence of header
    if not auth_header:
        raise AuthError({
            'code': 'missing_authorization_header',
            'description': 'Expected Authoriation header'
        }, 401)

    # validate authn format
    header_parts = auth_header.split(' ')

    if not len(header_parts) ==2:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization header needs 2 parts'
        }, 401)

    if header_parts[0].lower() != 'bearer':
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization header should start with "bearer"'
        }, 401)

    token = header_parts[1]
    return token

# Verify JWT token

#get jwt from Auth0
def verify_code_jwt(token):
    jsonurl = urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
    jwks = json.loads(jsonurl.read())

    #get data in header
    unverified_header = jwt.get_unverified_header(token)

    #choose key
    if 'kid' not in unverified_header:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization malformed'
        }, 401)

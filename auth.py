import os
import json
from os import execle
from flask import request, _request_ctx_stack, abort
from functools import wraps
from jose import jwt
from urllib.request import urlopen

AUTH0_DOMAIN = os.getenv.get('AUTH0_DOMAIN')
ALGORITHMS = os.getenv.get('ALGORITHMS')
API_AUDIENCE = os.getenv.get('API_AUDIENCE')

## AuthError Exception
# Standardized method to communicate failure modes

class AuthError(Exception):
    def __init__(self, error, status_code):
       self.error = error
       self.status_code = status_code

## Auth Header
# Get header from request
def get_token_auth_header():
    auth_header = request.headers.get('Authorization', None)

    # check for presence of header
    if not auth_header:
        raise AuthError({
            'code': 'missing_authorization_header',
            'description': 'Expected Authorization header'
        }, 401)

    # validate authn format of bearer +token
    header_parts = auth_header.split(' ')

    if not len(header_parts) ==2:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization header needs 2 parts'
        }, 401)

    if header_parts[0].lower() != 'bearer':
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization header should start with Bearer'
        }, 401)

    token = header_parts[1]
    return token

### Check permissions of decoded payload (RBAC settings)
def check_permissions(permission, payload):
    if 'permissions' not in payload:
        raise AuthError({
            'code': 'invalid_claims',
            'description': 'Permissions not included'
            }, 400)
    
    if permission not in payload['permissions']:
        raise AuthError({
            'code': 'unauthorized',
            'description': 'Permission not found' 
            }, 403)

    return True

# Verify JWT token
#get jwt from Auth0
def verify_decode_jwt(token):
    jsonurl = urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
    jwks = json.loads(jsonurl.read())

    #get data in header
    unverified_header = jwt.get_unverified_header(token)
    rsa_key = {}
    #choose key
    if 'kid' not in unverified_header:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization malformed'
        }, 401)

    for key in jwks['keys']:
        if key['kid'] == unverified_header['kid']:
            rsa_key = {
                'kty': key['kty'],
                'kid': key['kid'],
                'use': key['use'],
                'n': key['n'],
                'e': key['e']
            }

    #verify - use key to validate jwt
    if rsa_key:
        try:
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms = ALGORITHMS,
                audience = API_AUDIENCE,
                issuer='https://' + AUTH0_DOMAIN + '/'
            )

            return payload

        except jwt.ExpiredSignatureError:
            raise AuthError({
                'code': 'token_expired',
                'description': 'Token expired'
            }, 401)

        except jwt.JWTClaimsError:
            raise AuthError({
                'code': 'invalid_claims',
                'description': 'Invalid claims. Please check audience and issuer'
            }, 400)
        
        except Exception:
            raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to parse authentication token'
            }, 400)

    raise AuthError({
        'code': 'invalid_header',
        'description': 'Unable to find appropriate key'
    }, 400)

### Authn permission requirement 
def requires_auth(permission=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = get_token_auth_header()
            payload = verify_decode_jwt(token)
            check_permissions(permission, payload)
            return f(payload, *args, **kwargs)

        return wrapper
    return requires_auth_decorator

from flask import Flask, request, abort, jsonify
import json
from functools import wraps
from jose import jwt
from urllib.request import urlopen
from jose import jwt
from urllib.request import urlopen
import json

# https://dev-z8uvjzxy.us.auth0.com/authorize?audience=image&response_type=token&client_id=GXJtygYptWDRJvPLAbbtZKihiNpm5bew&redirect_uri=https://127.0.0.1:8080/home
app = Flask(__name__)

AUTH0_DOMAIN = 'dev-z8uvjzxy.us.auth0.com'
ALGORITHMS = ['RS256']
API_AUDIENCE = 'image'


class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


def get_token_auth_header():
    """Obtains the Access Token from the Authorization Header
    """
    auth = request.headers.get('Authorization', None)
    if not auth:
        raise AuthError({
            'code': 'authorization_header_missing',
            'description': 'Authorization header is expected.'
        }, 401)

    parts = auth.split()
    if parts[0].lower() != 'bearer':
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization header must start with "Bearer".'
        }, 401)

    elif len(parts) == 1:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Token not found.'
        }, 401)

    elif len(parts) > 2:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization header must be bearer token.'
        }, 401)

    token = parts[1]
    return token


def verify_decode_jwt(token):
    jsonurl = urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
    jwks = json.loads(jsonurl.read())
    unverified_header = jwt.get_unverified_header(token)
    rsa_key = {}
    if 'kid' not in unverified_header:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization malformed.'
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
    if rsa_key:
        try:
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                issuer='https://' + AUTH0_DOMAIN + '/'
            )

            return payload

        except jwt.ExpiredSignatureError:
            raise AuthError({
                'code': 'token_expired',
                'description': 'Token expired.'
            }, 401)

        except jwt.JWTClaimsError:
            raise AuthError({
                'code': 'invalid_claims',
                'description': 'Incorrect claims. Please, check the audience and issuer.'
            }, 401)
        except Exception:
            raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to parse authentication token.'
            }, 400)
    raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to find the appropriate key.'
            }, 400)

def check_permission(payload, permission=''):
    if 'permissions' not in payload:
        raise AuthError({
                        'code': 'invalid_claims',
                        'description': 'Permissions not included in JWT.'
                        }, 400)
    if permission not in payload['permissions']:
        raise AuthError({
            'code': 'unauthorized',
            'description': 'Permission not found.'
        }, 403)
    return True
    
        
        
def requires_auth(permission=''):
    def requires_auth_decor(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            # try:
            token = get_token_auth_header()
            payload = verify_decode_jwt(token)
            check_permission(payload, permission)
            # except:
            #     abort(401)
            return f(payload, *args, **kwargs)

        return wrapper
    return requires_auth_decor


@app.route('/images')
@requires_auth('get:images')
def images(payload):
    print(payload)
    print(payload['permissions'])
    return '{}\nAccess Granted'.format(payload)

@app.route('/')
def header():
    return "access granted!"

@app.errorhandler(AuthError)
def authError(authError):
    return jsonify({
        "success": False,
        "error": authError.status_code,
        "message": authError.error['description']
    }), authError.status_code
    


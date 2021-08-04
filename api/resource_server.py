import flask
from flask import Flask, request
from flask_restful import Api, Resource
from jose import jwt
import requests
import json
from functools import wraps
from config import API_SECURITY_LEVEL, API_NAME, HELSEID_METADATA_URL

app = Flask(__name__)
api = Api(app)

# Some API-data that is protected with HelseID access token
patient_data = {
    13109525611: {'name': 'Johannes', 'age': 25},
    19109355618: {'name': 'Sigrid', 'age': 27},
    10109925624: {'name': 'Olav', 'age': 21},
    13099845614: {'name': 'Oda', 'age': 22},
    17107023612: {'name': 'Vegard', 'age': 51}
}

# Cache metadata from HelseID
helseid_metadata = json.loads(requests.get(HELSEID_METADATA_URL).text)
jwks = json.loads(requests.get(helseid_metadata['jwks_uri']).text)
algorithms = [key['alg'] for key in jwks['keys']]


def get_token_auth_header():
    """Extracts the Access Token from the Authorization Header."""
    auth = request.headers.get('Authorization', None)
    if not auth:
        raise Exception('authorization_header_missing - Authorization header is expected')
    parts = auth.split()
    if parts[0].lower() != 'bearer':
        raise Exception('authorization_header_missing - Authorization header must start with Bearer')
    elif len(parts) == 1:
        raise Exception('invalid_header - Token not found')
    elif len(parts) > 2:
        raise Exception('invalid_header - Authorization header must be Bearer token')
    token = parts[1]
    return token


def get_rsa_key(kid):
    """Get the RSA key from metadata based on kid
     Args:
        kid (str): The kid to look up rsa key values from
    """
    for key in jwks['keys']:
        if key['kid'] == kid:
            rsa_key = key
            return rsa_key
    raise Exception('key_not_found - kid did not match any key from metadata')


def validate_access_token(access_token, rsa_key):
    """Verify an access token with the provided rsa_key.
    Args:
        access_token (str): A JWT access token
        rsa_key (dict): The key to verify the payload
    """
    # Set required claims you expect in the access token payload
    options = {
        'require_aud': True,
        'require_iat': True,
        'require_exp': True,
        'require_nbf': True,
        'require_iss': True,
        'require_jti': True
    }
    # Validate JWT signature and validate claims, payload is set if succeeded
    payload = jwt.decode(
        token=access_token,
        key=rsa_key,
        algorithms=algorithms,
        options=options,
        audience=API_NAME,
        issuer=helseid_metadata['issuer']
    )
    # Validate only 1 audience in access token (OPTIONAL)
    if type(payload['aud']) == list and len(payload['aud']) > 1:
        raise Exception(f'invalid_claims - Nr. of audience should be 1, but was {len(payload["aud"])}')

    # Validate security level of user (ONLY WORKS WITH ACCESS TOKENS CONTAINING USER INFO)
    '''
    token_security_level = int(payload.get('helseid://claims/identity/security_level', -1))
    if token_security_level < API_SECURITY_LEVEL:
        raise Exception('invalid_claims - User is not authorized to view this data. Check users security level')
    '''

def requires_auth(f):
    """Determines if the Access Token is valid and user should be granted access."""
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            access_token = get_token_auth_header()
            unverified_header = jwt.get_unverified_header(access_token)
            rsa_key = get_rsa_key(unverified_header['kid'])
            if rsa_key:
                validate_access_token(access_token, rsa_key)
                return f(*args, **kwargs)
            raise Exception('invalid_header - Unable to find appropriate key')
        except Exception as e:
            flask.abort(401, str(e))
    return decorated


def requires_scope(required_scope):
    """Determines if the access token contains the required scope of the resource
    Args:
        required_scope (str): The scope protecting the resource
    """
    def decorator(f):
        def wrapper(*args, **kwargs):
            access_token = get_token_auth_header()
            unverified_claims = jwt.get_unverified_claims(access_token)
            if unverified_claims.get('scope'):
                token_scopes = unverified_claims['scope']
                for scope in token_scopes:
                    if scope == required_scope:
                        return f(*args, **kwargs)
            flask.abort(401, "You don't have access to this resource")
            return f(*args, **kwargs)
        return wrapper
    return decorator


class PatientList(Resource):
    @requires_auth
    @requires_scope("norsk-helsenett:python-sample-api/read")
    def get(self):
        return patient_data, 200


api.add_resource(PatientList, '/api/patients')

if __name__ == '__main__':
    app.run(debug=True)

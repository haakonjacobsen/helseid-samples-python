import json
import base64
import requests
import pkce
import time

from functools import wraps
from werkzeug.exceptions import HTTPException
from flask import Flask, jsonify, redirect, render_template, session, url_for
from authlib.integrations.flask_client import OAuth
from authlib.jose import jwt
from urllib.parse import urlencode
from uuid import uuid4

from config import CLIENT_ID, HELSEID_METADATA_URL, PRIVATE_KEY

# ATTENTION:
# THIS EXAMPLE USES HTTP FOR SIMPLICITY
# ALWAYS USE HTTPS IN DEPLOYMENT FOR YOUR WEB CLIENT

app = Flask(__name__, static_url_path='/public', static_folder='./public')
app.secret_key = 'ThisIsTheSecretKey'
app.debug = True

oauth = OAuth(app)

# Cache metadata from HelseID
helseid_metadata = json.loads(requests.get(HELSEID_METADATA_URL).text)

# Create an OAuth client with HelseID information
helseid = oauth.register(
    name='helseid',
    client_id=CLIENT_ID,
    server_metadata_url=HELSEID_METADATA_URL
)


def create_jwt_header():
    header = {
        'alg': PRIVATE_KEY['alg'],
        'kid': PRIVATE_KEY['kid']
    }
    return header


def create_client_assertion():
    """Creates and returns a signed JTW for client assertion"""
    now = int(time.time())
    payload = {
        'sub': CLIENT_ID,
        'iat': now,
        'jti': uuid4().hex,
        'nbf': now,
        'exp': now + 60,
        'iss': CLIENT_ID,
        'aud': helseid_metadata['token_endpoint']
    }
    header = create_jwt_header()
    encoded = jwt.encode(header, payload, PRIVATE_KEY)
    return encoded


def create_request_object(payload):
    """Creates and returns a request object
    Args:
        payload (dict): The payload to use in the JWT"""
    header = create_jwt_header()
    encoded = jwt.encode(header, payload, PRIVATE_KEY)
    return encoded


def b64_decode_jwt(token):
    """Base64 decodes a jwt in UTF-8 format. Returns three values:
    header, payload and signature"""
    token = token.split('.')
    if len(token) != 3:
        raise ValueError(f'Length of jwt should be 3, but was {len(token)}')
    for i in range(0, 2):
        # Pad header and payload for b64decoding
        token[i] = token[i] + ('=' * (len(token[i]) % 4))
    header = json.loads(base64.b64decode(token[0]).decode('UTF-8'))
    payload = json.loads(base64.b64decode(token[1]).decode('UTF-8'))
    return header, payload


def requires_auth(f):
    """Decide if user is logged in or should be logged out"""
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'id_token' not in session or 'end_time' not in session:
            return redirect('/')
        if session['end_time'] <= int(time.time()):
            return redirect(url_for('logout'))
        return f(*args, **kwargs)
    return decorated


# ---- Routes ----
@app.route('/')
def home():
    return render_template('home.html')


@app.route('/login-helseid')
def login_helseid():
    helseid_client = oauth.create_client('helseid')

    # Generate code verifier- and challenge with PKCE. Save verifier.
    code_verifier, code_challenge = pkce.generate_pkce_pair()
    session['code_verifier'] = code_verifier

    # Generate nonce
    session['nonce'] = uuid4().hex

    # Generate a JWT request_object to for passing parameters
    now = int(time.time())
    request_object_payload = {
        'scope': 'openid profile norsk-helsenett:python-sample-api/read',
        'client_id': CLIENT_ID,
        'iss': CLIENT_ID,
        'aud': helseid_metadata['issuer'],
        'nonce': session['nonce'],
        'code_challenge': code_challenge,
        'code_challenge_method': 'S256',
        'jti': uuid4().hex,
        'nbf': now,
        'exp': now + 60
    }
    request_object = create_request_object(request_object_payload)

    params = {
        'request': request_object
    }
    callback_url = url_for('callback', _external=True)

    # Redirect to HelseID with callback url and request object as parameter
    return helseid_client.authorize_redirect(callback_url, **params)


@app.route('/callback')
def callback():
    """The endpoint for exchanging the authorization code with access token"""
    helseid_client = oauth.create_client('helseid')

    # Exchange auth code with access- and ID-token
    params = {
        'code_verifier': session['code_verifier'],
        'client_assertion': create_client_assertion(),
        'client_assertion_type': 'urn:ietf:params:oauth:client-assertion-type:jwt-bearer'
    }
    response = helseid_client.authorize_access_token(**params)

    # Extract ID and access token
    id_token = response['id_token']
    access_token = response['access_token']

    # Decode ID token
    _header, payload = b64_decode_jwt(id_token)

    # Validate issuer
    if payload['iss'] != helseid_metadata['issuer']:
        print('Issuer did not match metadata')
        return redirect(url_for('home'))

    # Validate nonce
    if payload['nonce'] != session['nonce']:
        print('Nonce did not match')
        return redirect(url_for('home'))

    # Save information to session
    session['end_time'] = payload['exp']
    session['id_token'] = id_token
    session['access_token'] = access_token
    session['jwt_payload'] = payload
    session['api_data'] = {'Data': 'No data has been loaded yet'}

    return redirect('/dashboard')


@app.route('/logout')
def logout():
    params = {
        'id_token_hint': session['id_token'],
        'post_logout_redirect_uri': url_for('home', _external=True)
    }
    session.clear()
    return redirect(f'{helseid_metadata["end_session_endpoint"]}?{urlencode(params)}')


@app.route('/dashboard')
@requires_auth
def dashboard():
    return render_template('dashboard.html',
                           userinfo=session['jwt_payload'],
                           userinfo_pretty=json.dumps(session['api_data'], indent=4))


@app.route('/get_data')
@requires_auth
def get_api_data():
    try:
        header = {'Authorization': f'Bearer {session["access_token"]}'}
        session['api_data'] = json.loads(requests.get(
                                'http://localhost:5000/api/patients',
                                headers=header).text)
        return redirect('/dashboard')
    except Exception:
        session['api_data'] = 'Error: Not able to parse response from API.'


@app.errorhandler(Exception)
def handle_auth_error(ex):
    response = jsonify(message=str(ex))
    response.status_code = (ex.code if isinstance(ex, HTTPException) else 500)
    return response


if __name__ == "__main__":
    app.run(host='localhost', port=3000)

import json
import requests
import time

from functools import wraps
from werkzeug.exceptions import HTTPException
from flask import Flask, jsonify, redirect, render_template, session, url_for
from authlib.integrations.flask_client import OAuth
from authlib.jose import jwt
from urllib.parse import urlencode
from uuid import uuid4

from config import CLIENT_ID, HELSEID_METADATA_URL, SCOPES, API_BASE_URL, PRIVATE_KEY

# ATTENTION:
# THIS EXAMPLE USES HTTP FOR SIMPLICITY
# ALWAYS USE HTTPS IN DEPLOYMENT FOR YOUR WEB CLIENT

app = Flask(__name__, static_url_path='/public', static_folder='./public')
app.secret_key = 'ThisIsTheSecretKey'
app.debug = True

# Create an OAuth (OIDC) client with HelseID information.
oauth = OAuth(app)
oauth.register(
    name='helseid',
    client_id=CLIENT_ID,
    server_metadata_url=HELSEID_METADATA_URL,
    client_kwargs={'scope': SCOPES},
    api_base_url=API_BASE_URL,
    code_challenge_method='S256'
)
helseid_client = oauth.create_client('helseid')
helseid_metadata = helseid_client.load_server_metadata()


def create_jwt_header():
    """Creates a JWT header based on the clients private key"""
    header = {
        'alg': PRIVATE_KEY['alg'],
        'kid': PRIVATE_KEY['kid']
    }
    return header


def create_jwt_credentials(audience):
    """Creates and returns a signed JWT containing client information
    Args:
        audience (str): The audience of the JWT"""
    now = int(time.time())
    payload = {
        'sub': CLIENT_ID,
        'iat': now,
        'jti': uuid4().hex,
        'nbf': now,
        'exp': now + 60,
        'iss': CLIENT_ID,
        'aud': audience
    }
    header = create_jwt_header()
    encoded = jwt.encode(header, payload, PRIVATE_KEY)
    return encoded


def create_client_assertion():
    return create_jwt_credentials(helseid_metadata['token_endpoint'])


def create_request_object():
    return create_jwt_credentials(helseid_metadata['issuer'])



def requires_auth(f):
    """Decide if user is logged in or should be logged out"""
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'id_token' not in session:
            return redirect('/')
        return f(*args, **kwargs)
    return decorated


# ---- Routes ----
@app.route('/')
def home():
    if 'id_token' in session:
        return redirect('/dashboard')
    return render_template('home.html')


@app.route('/login-helseid')
def login_helseid():
    # Generate a JWT request_object for passing parameters
    request_object = create_request_object()

    # Redirect to HelseID with callback url and request object as parameter
    params = {
        'request': request_object
    }
    callback_url = url_for('callback', _external=True)
    return helseid_client.authorize_redirect(callback_url, **params)


@app.route('/callback')
def callback():
    """The endpoint for exchanging the authorization code with tokens"""
    params = {
        'client_assertion': create_client_assertion(),
        'client_assertion_type': 'urn:ietf:params:oauth:client-assertion-type:jwt-bearer'
    }
    response = helseid_client.authorize_access_token(**params)
    # Validate ID-token
    id_token_payload = helseid_client.parse_id_token(response, leeway=10)
    # Extract Access token
    access_token = response['access_token']
    # Save information to session
    session['id_token'] = response['id_token']
    session['access_token'] = access_token
    session['payload'] = id_token_payload
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
                           userinfo=session['payload'],
                           userinfo_pretty=json.dumps(session['api_data'], indent=4))


@app.route('/get_data')
@requires_auth
def get_api_data():
    try:
        header = {'Authorization': f'Bearer {session["access_token"]}'}
        session['api_data'] = json.loads(requests.get(
                                'http://localhost:5000/api/patients',
                                headers=header).text)
    except Exception as ex:
        session['api_data'] = { ex.__class__.__name__: str(ex.args)}
    return redirect('/dashboard')


@app.errorhandler(Exception)
def handle_auth_error(ex):
    response = jsonify(message=str(ex))
    response.status_code = (ex.code if isinstance(ex, HTTPException) else 500)
    return response


if __name__ == "__main__":
    app.run(host='localhost', port=3000)
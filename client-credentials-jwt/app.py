import requests
import json
import time
from authlib.jose import jwt
from uuid import uuid4

from config import CLIENT_ID, HELSEID_METADATA_URL, RESOURCE_URI, PRIVATE_KEY

# Cache metadata from HelseID
helseid_metadata = json.loads(requests.get(HELSEID_METADATA_URL).text)


def create_client_assertion():
    """Creates and returns a signed JTW for client assertion"""
    header = {
        'alg': PRIVATE_KEY['alg'],
        'kid': PRIVATE_KEY['kid']
    }
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
    encoded = jwt.encode(header, payload, PRIVATE_KEY)
    return encoded


def get_helseid_access_token():
    """Request an access token from HelseID using the
    client credentials flow"""
    try:
        params = {
            'client_id': CLIENT_ID,
            'grant_type': 'client_credentials',
            'scope': 'norsk-helsenett:python-sample-api/read',
            'client_assertion': create_client_assertion(),
            'client_assertion_type': 'urn:ietf:params:oauth:client-assertion-type:jwt-bearer'
        }
        response = requests.post(
                    helseid_metadata['token_endpoint'],
                    data=params)
        if 'access_token' in response.json():
            access_token = response.json()['access_token']
            return access_token
        else:
            print('error, the request did not return a access token')
            return 
    except ConnectionError as e:
        print('Could not connect to server', e)
    except Exception as e:
        print('Could not get a response', e)


def get_api_data(access_token):

    try:
        response = requests.get(RESOURCE_URI,
                                headers={'Authorization': f'Bearer {access_token}'})
        data = json.loads(response.text)
        response_code = response.status_code
        return data, response_code
    except ConnectionError as e:
        print('Not able to connect to the API.' + str(e))
    except Exception as e:
        print('Not able to get data from API. Error: ' + str(e))


def main():
    access_token = get_helseid_access_token()
    print(f'Access token: {access_token}')

    data, response_code = get_api_data(access_token)
    print('\nResponse')
    print(f'Status code: {response_code}')
    print(f'Data: {data}')


if __name__ == "__main__":
    main()

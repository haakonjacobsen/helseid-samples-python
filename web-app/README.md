# HelseID sample web app in Python

This sample demonstrates how to add authentication to a basic Python web app (Flask) using the OAuth 2.0 authorization code flow with HelseID. The application runs out of the box and you can implement your own client information later.

## Running the App
To run the sample, make sure you have `python` and `pip` installed (using a virtual environment is recommended).

From the `../web-app` folder:

Install dependencies:
```
pip install -r requirements.txt
```

Run application (Windows):
```
py app.py
```
Run application (Mac/Linux):
```
python3 app.py
```

The app will be served at [http://localhost:3000](http://localhost:3000).

## API connection
To receive data in the application, you need to run the [API example](https://github.com/haakonjacobsen/helseid-samples-python/tree/master/api) aswell. Follow the setup on that page to get the API up and running. 

## Register a client
If you want to implement your own client you first need to register it at HelseID admin. Here you will get a `client_id` and you can define `scopes` for the application. For a web application, the scopes `openid` and `profile` are both required. In the client at HelseID you would want to register `http://localhost:3000/callback` in the `Redirect URIs` and `http://localhost:3000` as `Post logout redirects URIs`. In `config.py` you need to change the `CLIENT_ID` to the one you recieved from HelseID admin, and change the `PRIVATE_KEY` and `PUBLIC_KEY` to your own key pair. You can use the sample key pair for JWT in the `config.py` file for testing purposes. DO NOT use this in development. Se next section on how to genereate your own key pair.

## Generate key pair for JWT
There are lots of ways to generate a key pair for JWK. You can generate one at [mkjwk.org](https://mkjwk.org/).

1. Choose a Key Size >= 2048
2. Key Use = Signature
3. Algorithm = PS256 (recommended) or RS256 (not recommended)
4. Key ID = SHA-256
5. Show X.509 = NO and click generate
6. Copy the Public and Private Keypair and paste is as the value of PRIVATE_KEY in `config.py`.
7. Copy the Public Key and paste is as the value of PUBLIC_KEY in `config.py`.
8. Register the Public Key in your clients client secrets in HelseID Admin as a JSON Web Key.

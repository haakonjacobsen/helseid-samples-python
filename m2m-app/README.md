# HelseID Python Sample for Machine to Machine Application

This sample demonstrates how to add HelseID authorization to a Python machine to machine (m2m) app using the OAuth 2.0 client credentials flow with JSON Web Tokens (JWT). The application runs out of the box and you can implement your own client information later.

## Running the App
To run the sample, make sure you have `python` and `pip` installed (using a virtual environment is recommended).

From the `../m2m-app` folder:

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
pyhon3 app.py
```

2. Run `python3 app.py` on Mac/Linux or `py app.py` on Windows (assuming this is how your python 3 is configured).

## API connection
To receive data in the application, you need to run the [API example](https://github.com/haakonjacobsen/helseid-samples-python/tree/master/api) aswell. Follow the setup on that page to get the API up and running. 

## Register a client
If you want to implement your own client you first need to register it at HelseID admin. Here you will get a `client_id` and you can define `scopes` for the application. For a m2m application you can use the `norsk-helsenett:python-sample-api/read` for testing aginst the [API sample](https://github.com/haakonjacobsen/helseid-samples-python/tree/master/api). In `config.py` you need to change the `CLIENT_ID` to the one you recieved from HelseID admin and change the `PRIVATE_KEY` and `PUBLIC_KEY` to your own key pair. You can use the sample key pair for JWT in the `config.py` file for testing purposes. DO NOT use this in development. Se next section on how to genereate your own key pair.

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

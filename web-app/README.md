# HelseID Python Web App Sample

This sample demonstrates how to add authentication to a Python web app (Flask) using the OAuth 2.0 authorization code flow with HelseID. The application runs out of the box and you can implement your own client information later.

## Running the App
To run the sample, make sure you have `python` and `pip` installed (using a virtual environment is recommended).

From the `../web-app` folder:

1. Run `pip install -r requirements.txt` to install the dependencies. 

2. Run `python3 app.py` on Mac/Linux or `py app.py` on Windows (assuming this is how your python 3 is configured).

The app will be served at [http://localhost:3000](http://localhost:3000).

## API connection
To recive data in the application, you need to run the [API example](https://github.com/haakonjacobsen/helseid-samples-python/tree/master/api) aswell. Follow the setup on that page to get the API up and running. 

## Register a client
If you want to implement your own client you first need to register it at HelseID admin. Here you will get a `client_id` and you can define `scopes` for the application. For a web application, the scopes `openid` and `profile` are both required. You should also set up your `JWK public key` and other settings. You can use the a sample information for JWK in the `config.py` file, but DO NOT use this in development, you need to generate your own. 

In the client at HelseID you would want to register `http://localhost:3000/callback` in the `Redirect URIs` and `http://localhost:3000` as `Post logout redirects URIs`. In the application you need to change the `CLIENT_ID` to the one you recieved from HelseID admin, and change the `PRIVATE_KEY` and `PUBLIC_KEY` to 

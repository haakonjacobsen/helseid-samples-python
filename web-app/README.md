# HelseID Python Web App Sample

This sample demonstrates how to add authentication to a Python web app using HelseID.

## Register a client
The application runs out of the box, and you can skip this next section if you just want to run the application. If you want to implement your own client, you first need to register it at HelseID admin. Here you would get a `Client_ID` and you can define `scopes` for the application. You should also set up your `JWK public key` and other settings. You can use the a sample information for JWK from the provided `jwk_info.py` file. In the client you would want to register `http://localhost:3000/callback` in the `Redirect URIs` and `http://localhost:3000` as `Post logout redirects URIs`. In the application you need to change the `CLIENT_ID` to the one you recieved from HelseID admin, and change the `jwt_private_key.txt` to your own in PEM format.

## Running the App
To run the sample, make sure you have `python` and `pip` installed. Once the client is setup properly (or just use the example provided) you can Run `pip install -r requirements.txt` to install the dependencies and run `python server.py`. 
The app will be served at [http://localhost:3000/](http://localhost:3000/).

## API connection
To recive data in the application, you need to run the [API example](https://github.com/haakonjacobsen/HelseID_api)
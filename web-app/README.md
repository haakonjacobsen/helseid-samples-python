# HelseID sample web app in Python

This sample demonstrates how to add authentication to a basic Python web app (Flask) using the OAuth 2.0 authorization code flow with HelseID. 
The application runs out of the box with sample clients registered in HelseID development.

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

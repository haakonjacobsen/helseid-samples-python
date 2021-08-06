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
python3 app.py
```

## API connection
To receive data in the application, you need to run the [API example](https://github.com/haakonjacobsen/helseid-samples-python/tree/master/api) aswell. Follow the setup on that page to get the API up and running. 

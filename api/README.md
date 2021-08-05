## Python (Flask RESTful) sample for protecting an API with HelseID
Explaintion

## Running the API
To run the API, make sure you have `python` and `pip` installed (using a virtual environment is recommended).

From the `../api` folder:

Install dependencies:
```
pip install -r requirements.txt
```

Run application (Windows):
```
py resource_server.py
```
Run application (Mac/Linux):
```
python3 resource_server.py
```

The API will be served at http://localhost:5000/api/

## Endpoints
The API has 1 endpoint which returns mock data of patient information in JSON format:

1.  The endpoint http://localhost:5000/api/patients requires a valid access token issued by HelseID cluding the scope `norsk-helsenett:python-sample-api/read`.
To access the data you have to send a GET request to with the access token in the Authroization header with the value "Bearer <ACCESS_TOKEN>". The API will validate the access token and return the data if the access token is valid. 

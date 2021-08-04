## Python (Flask RESTful) sample for protecting an API with HelseID
Explaintion

## Running the API
To run the API, make sure you have `python` and `pip` installed (using a virtual environment is recommended).

From the `../api` folder:

1. Run `pip install -r requirements.txt` to install the dependencies. 

2. Run `python3 resource_server.py` on Mac/Linux or `py resource_server.py` on Windows (assuming this is how your python 3 is configured).

The API will be served at 

## Endpoints
The API has 1 endpoint which returns mock data of patient information in JSON format:

1.  The endpoint http://localhost:5000/api/patients requires a valid access token issued by HelseID cluding the scope `norsk-helsenett:python-sample-api/read`.
To access the data you have to send a GET request to with the access token in the Authroization header with the value "Bearer <ACCESS_TOKEN>". The API will validate the access token and return the data if the access token is valid. 

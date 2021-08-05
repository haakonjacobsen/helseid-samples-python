# HelseID Samples in Python
HelseID is a national authentication service for the health sector in Norway. These samples are targeted at technical personnel such as application architects and developers on how to implement HelseID in Python applications. The samples consists of 3 applications.

## [Web App](web-app)
The web app demonstrates the authorization code flow (openID connect). It uses the id token to verify the identity of the user. It also gets an access token, which it uses to retrieve a resource from the [API](api).

## [Machine to machine](client-crentials-jwt)
The m2m app uses the client credentials flow (OAuth 2.0) to get an access token, and uses the access token retrieve a resource from the [API](api).

## [API](api)
The API provides simple mock data protected with HelseID. To retrive data the user must provide a valid access token issued by HelseID in the header of a GET request.


More info on https://nhn.no/helseid/ (Norwegian) and https://dokumentasjon.helseid.no/

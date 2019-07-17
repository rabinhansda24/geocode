import requests
import googlemaps
import ast
import json

#Google API key
key = ''
gmaps = googlemaps.Client(key=key)


def get_geocode(address):
    #Get the GeoCode of the address
    geocode_result = gmaps.geocode(address)
    #Convert the resultset into dictionary
    data = ast.literal_eval(json.dumps(
        geocode_result[0]['geometry']['location']))
    lat = data['lat']
    lang = data['lng']
    return lat, lang


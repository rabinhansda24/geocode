import requests
import googlemaps
import ast
import json

#Google API key
key = 'AIzaSyDMs7fNkk-vW7i4-VDVmkezikm6MAGP93M'
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


# Useful URLs (you need to add the appropriate parameters for your requests)
MAPQUEST_BASE_URL = "http://www.mapquestapi.com/geocoding/v1/address"
MBTA_BASE_URL = "https://api-v3.mbta.com/stops"

# Your API KEYS (you need to use your own keys - very long random characters)
MAPQUEST_API_KEY = "b8jrbsNBSZFgAC8cMfDt0przdvKkAlOK"
MBTA_API_KEY = "30140eb3ff944e4e80bdc9cb3aaf1e80"

import pprint
import urllib.request
import json

# A little bit of scaffolding if you want to use it


def get_json(url):
    """
    Given a properly formatted URL for a JSON web API request, return
    a Python JSON object containing the response to that request.
    """

    f = urllib.request.urlopen(url)
    response_text = f.read().decode("utf-8")
    response_data = json.loads(response_text)
    return response_data


def get_lat_long(place_name):
    """
    Given a place name or address in MA, return a (latitude, longitude) tuple
    with the coordinates of the given place.
    See https://developer.mapquest.com/documentation/geocoding-api/address/get/
    for Mapquest Geocoding  API URL formatting requirements.
    """

    place_name = place_name.replace(" ", "%20")
    if not "MA" in place_name:
        place_name += ",MA"
    # print(place_name)
    url = f"http://www.mapquestapi.com/geocoding/v1/address?key={MAPQUEST_API_KEY}&location={place_name}"
    response_data = get_json(url)
    # print(url)
    # pprint.pprint(response_data)
    lat = response_data["results"][0]["locations"][0]["latLng"]["lat"]
    lng = response_data["results"][0]["locations"][0]["latLng"]["lng"]
    return (lat, lng)


def get_nearest_station(latitude, longitude):
    """
    Given latitude and longitude strings, return a (station_name, wheelchair_accessible)
    tuple for the nearest MBTA station to the given coordinates.
    See https://api-v3.mbta.com/docs/swagger/index.html#/Stop/ApiWeb_StopController_index for URL
    formatting requirements for the 'GET /stops' API.
    """
    url = f"https://api-v3.mbta.com/stops?sort=distance&api_key={MBTA_API_KEY}&filter[latitude]={latitude}&filter[longitude]={longitude}&filter[radius]=2"
    response_data = get_json(url)
    # print(response_data)
    try:
        name = response_data["data"][0]["attributes"]["name"]
        wheelchair = response_data["data"][0]["attributes"]["wheelchair_boarding"]
        return name, wheelchair
    except IndexError as e:
        name = "No location found"
        wheelchair = 0
        return name, wheelchair


def find_stop_near(place_name):
    """
    Given a place name or address, enter whether to display wheelchair accesibility, return the nearest MBTA stop and whether it is wheelchair accessible.
    """
    wheelchair_list = ["not clear if it is accessible", "accessible", "inaccessible"]
    latitude, longitude = get_lat_long(place_name)
    name, n = get_nearest_station(latitude, longitude)
    return name, wheelchair_list[n]


def main():
    """
    You can test all the functions here
    """
    # latitude, longitude = get_lat_long("Boston Common")
    # print(latitude, longitude)
    # print(get_nearest_station(latitude, longitude))
    print(find_stop_near("Boston Common"))


if __name__ == "__main__":
    main()

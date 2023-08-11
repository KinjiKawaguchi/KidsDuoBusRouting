import requests
import json
from urllib.parse import quote


class GoogleMapsClient:
    def __init__(self, api_key):
        self.API_KEY = api_key

    def calculate_duration(self, from_address, to_address):
        """
        Calculates the duration and distance between two addresses using the Google Maps API.

        :param from_address: Starting address
        :param to_address: Destination address
        :return: Tuple containing duration and distance, or (None, None) if an error occurs
        """
        # URL-encode the addresses
        origin = quote(from_address)
        destination = quote(to_address)

        # Construct the API request URL
        url = f"https://maps.googleapis.com/maps/api/distancematrix/json?origins={origin}&destinations={destination}" \
              f"&key={self.API_KEY}"

        # Execute the API request
        response = requests.get(url)

        # Parse the response into JSON format
        data = json.loads(response.text)

        # Extract the duration and distance from the response
        try:
            duration = data["rows"][0]["elements"][0]["duration"]["text"]
            distance = data["rows"][0]["elements"][0]["distance"]["text"]
        except KeyError:
            print("Error: Unable to retrieve duration and distance.")
            duration, distance = None, None

        return duration, distance

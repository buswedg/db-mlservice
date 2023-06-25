import googlemaps
import logging
from django.conf import settings
from googlemaps.exceptions import ApiError

logger = logging.getLogger('custom')


class GmapHandler:
    """
    A module to handle Google Maps API related operations.
    """

    def __init__(self, api_key=None):
        self.api_key = api_key or settings.GOOGLE_MAPS_KEY
        self.gmaps = googlemaps.Client(key=self.api_key)

    def geocode(self, address):
        try:
            return self.gmaps.geocode(address=address)
        except ApiError as e:
            print(f"Gmap Service: An error occurred while geocoding address: {e}")
            return None

    def reverse_geocode(self, lat, lng):
        try:
            return self.gmaps.reverse_geocode((lat, lng))
        except ApiError as e:
            print(f"Gmap Service: An error occurred while reverse geocoding: {e}")
            return None

    def find_place(self, text_query):
        try:
            return self.gmaps.find_place(
                text_query,
                'textquery',
                fields=['geometry/location'],
            )
        except ApiError as e:
            print(f"Gmap Service: An error occurred while finding place: {e}")
            return None

    def get_point_from_geocode(self, geocode_result):
        try:
            lat = geocode_result[0]['geometry']['location']['lat']
            lng = geocode_result[0]['geometry']['location']['lng']
            lat, lng = float(lat), float(lng)

            if lat != 0 or lng != 0:
                return lat, lng

        except (IndexError, KeyError) as e:
            logger.error(f"Gmap Service: An error occurred while getting point from geocode: {e}")

        return None

    def get_formatted_address_from_geocode(self, geocode_result):
        try:
            return geocode_result[0]['formatted_address']
        except (IndexError, KeyError) as e:
            logger.error(f"Gmap Service: An error occurred while getting formatted address from geocode: {e}")

        return None

    def get_parsed_address_from_geocode(self, geocode_result):
        try:
            address_components = geocode_result[0]['address_components']

            address = {}
            for component in address_components:
                if 'street_number' in component['types']:
                    address['street_number'] = component['long_name']
                if 'route' in component['types']:
                    address['street'] = component['long_name']
                if 'locality' in component['types']:
                    address['city'] = component['long_name']
                if 'administrative_area_level_1' in component['types']:
                    address['state'] = component['short_name']
                if 'country' in component['types']:
                    address['country'] = component['long_name']
                if 'postal_code' in component['types']:
                    address['zip_code'] = component['long_name']

            return address

        except (IndexError, KeyError) as e:
            logger.error(f"Gmap Service: An error occurred while getting parsed address from geocode: {e}")

        return None

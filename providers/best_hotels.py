import json
import os
from datetime import datetime as dt

from providers.provider_interface import ProviderInterface
from request_wrapper import RequestWrapper


class Besthotels(ProviderInterface):
    """
    This is an implementation of a provider called Best Hotels. It is derived from our Interface
    therefore our main API method `get_hotels` has got to be available here.
    """

    def get_hotels(self, from_date, to_date, city, adults):
        """
        Takes in the required parameters, arranges them into a dict which is required by the provider API
        Hits the API, gets results and them sends them to a formatted method.
        :param from_date: Datetime
        :param to_date: Datetime
        :param city: str
        :param adults: int
        :return: list
        """

        # RequestWrapper is an abstraction over requests post and get module.
        # This is to handle all exception which might be thrown by APIs.
        status_code, response = RequestWrapper().make_request(
            'post',
            os.environ.get("BEST_HOTELS_URL", ""),  # Takes in the Best Hotels API url from environment variables.
            {
                "city": city,
                "fromDate": dt.strftime(from_date, "%Y-%m-%d"),
                "toDate": dt.strftime(to_date, "%Y-%m-%d"),
                "numberOfAdults": adults
            }
        )

        return self.format_response(response) if status_code else []

    @staticmethod
    def format_response(response):
        """
        Takes in the HTTP response from our API, filters out data from it
        and sends them back to the client after arranging them into a unified format
        :param response: object of HTTP response class
        :return: list
        """

        if not response.ok:
            return []

        try:
            results = json.loads(response.text)
        except json.JSONDecodeError:
            return []

        hotels = []
        for result in results:
            hotel_name = result.get("hotel", None)
            price = result.get("hotelFare", None)
            amenities = result.get("roomAmenities", None)
            rate = result.get("hotelRate", None)

            if None in [hotel_name, price, amenities, rate]:
                # Woah we've got something unexpected here. Best idea might be to log it.
                print("Invalid response received from Best Hotels!")
                continue

            hotels.append({
                "provider": "Best Hotels",
                "hotelName": hotel_name,
                "fare": price,
                "amenities": [i.strip() for i in amenities.split(",")],  # We're expecting the amenities to be a str
                "rate": int(rate)
            })

        return hotels

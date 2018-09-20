"""
Please visit best_hotels.py before visiting this file as the comments are more extensively written there.
"""
import json
import os
from datetime import datetime as dt

from providers.provider_interface import ProviderInterface
from request_wrapper import RequestWrapper


class Crazyhotels(ProviderInterface):
    @staticmethod
    def _get_price(price, discount):
        """
        Accepts hotel price either float, int or str, deducts the discount value from it
        and returns a float value rounded off to two digits.
        :param price: float|int|str
        :param discount: float|int|str
        :return: float or 0
        """
        try:
            return max(round(float(price) - float(discount), 2), 0)
        except ValueError:
            return 0

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
        status_code, response = RequestWrapper().make_request(
            'post',
            os.environ.get("CRAZY_HOTELS_URL", ""),
            {
                "city": city,
                "from": dt.strftime(from_date, "%Y-%m-%dT%H:%M:%SZ"),
                "To": dt.strftime(to_date, "%Y-%m-%dT%H:%M:%SZ"),
                "adultsCount": adults
            }
        )

        return self.format_response(response) if status_code else []

    def format_response(self, response):
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
            hotel_name = result.get("hotelName", None)
            price = result.get("price", None)
            discount = result.get("discount", 0)
            amenities = result.get("amenities", None)
            rate = result.get("rate", None)

            if None in [hotel_name, price, amenities]:
                continue

            hotels.append({
                "provider": "Crazy Hotels",
                "hotelName": hotel_name,
                "fare": self._get_price(price, discount),
                "amenities": amenities,
                "rate": max(rate.count("*"), 1),  # We're expecting the rate to be a string with * (asterisks)
            })

        return hotels

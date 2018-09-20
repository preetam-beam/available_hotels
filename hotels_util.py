import importlib
from operator import itemgetter


class HotelsUtil:
    """
    This is our wrapper to all other provider api implementations.
    """
    def __init__(self, provider_list):
        """
        List of all implemented providers should be given while instantiating the class object.
        :param provider_list:
        """
        self.providers = provider_list

    @staticmethod
    def get_provider(provider_name):
        """
        Takes in provider name as string and returns it's class Object
        :param provider_name: str
        :return: Class Object
        """

        # Here's something to remember. All module file names should be lower cased
        # and the class names should be Title cased.
        # for example module could be hotels_of_paris but the class name can only be Hotelofparis
        provider_class = provider_name.replace("_", "").title()

        try:
            # Import the provider module from `providers` directory
            module = importlib.import_module("providers." + provider_name)
        except ModuleNotFoundError:
            # The module with given name is not implemented yet.
            return None

        try:
            # Get class definition of the given module.
            class_def = getattr(module, provider_class)
            return class_def()
        except AttributeError:
            # So the provider implementation didn't follow our convention.
            return None

    def get_all_hotels(self, from_date, to_date, city, adults):
        """
        Takes in parameters given to the API, visits all provider APIs and returns a comprehensive list of all hotels.
        :param from_date: Datetime
        :param to_date: Datetime
        :param city: str
        :param adults: Int
        :return: list
        """
        hotels = []

        # Loop through all providers
        for provider_name in self.providers:
            # Get Provider class object
            provider = self.get_provider(provider_name)

            if provider:
                # Visit their API, fetch results and append them to our hotels list.
                hotels += provider.get_hotels(from_date, to_date, city, adults)

        if hotels:
            # Sort our results based on hotes' ratings.
            hotels = sorted(hotels, key=itemgetter('rate'), reverse=True)

        for hotel in hotels:
            # We don't want rate to be displayed in our API response.
            del hotel['rate']

        return hotels


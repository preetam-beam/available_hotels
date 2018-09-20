"""
This is an Interface to be extended by all Providers, new integrations should be done by extending it.
"""


class ProviderInterface:
    def get_hotels(self, from_date, to_date, city, adults):
        """
        Abstract method, throws exception if not implemented.
        """
        raise NotImplementedError

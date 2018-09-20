import requests
import json


class RequestWrapper:
    """
    This is a wrapper to requests calls to handle some of the commonly occurred exceptions.
    """
    @staticmethod
    def _request_call(method, url, data, headers):
        """
        Calls the API endpoint's given method
        :param method: str
        :param url: str
        :param data: json dump
        :param headers: dict
        :return: HTTP response
        """
        if method == "get":
            return requests.get(
                url,
                headers=headers
            )
        else:
            return requests.post(
                url,
                json.dumps(data),
                headers=headers
            )

    def make_request(self, method, url, data, headers=None):
        """
        This is the entry method to our wrapper.
        :param method: str (method of the api to be called)
        :param url: str
        :param data: dict or could be None
        :param headers: dict or None
        :return: Tupple with (Boolean, HTTP response)
        """
        if not headers:
            headers = {'Content-Type': 'application/json'}

        try:
            response = self._request_call(
                method,
                url,
                data,
                headers
            )
        except requests.HTTPError:
            return False, "HTTP Error"
        except requests.ConnectionError:
            return False, "Connection Error"
        except requests.Timeout:
            return False, "Request Timeout"

        return True, response

import json
from datetime import datetime as dt
from flask import Flask, request
from hotels_util import HotelsUtil

app = Flask(__name__)

# Here's a list of all the providers we've got our integration done with.
# it can be kept in a config file (a YAML file for example) but for simplicity I've kept it as a list
# which is passed to our own API method.
provider_list = ['best_hotels', 'crazy_hotels']


def convert_date(date_str):
    """
    Converts Date String to Datetime Object
    :param: string (date)
    :return: Datetime|None
    """
    try:
        return dt.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        return None


@app.route('/get_hotels/', methods=['POST'])
def get_hotels():
    """
    Our API endpoint. Only accepts POST requests.
    Takes in four parameters - fromDate, toDate, city, numberOfAdults
    :return: JSON object with status: boolean, hotels: list and message: str
    """
    request_data = json.loads(request.data)

    from_date = convert_date(request_data.get("fromDate", None))
    to_date = convert_date(request_data.get("toDate", None))
    city = request_data.get("city", None)
    adults = request_data.get("numberOfAdults", None)

    response = {'status': True, 'hotels': [], 'message': ''}

    if None not in [from_date, to_date, city, adults]:
        response['hotels'] = HotelsUtil(provider_list).get_all_hotels(from_date, to_date, city, adults)
    else:
        # If any of the given parameters isn't valid or given then return an error
        response = {'status': False, 'hotels': [], 'message': 'Invalid parameters in request!'}

    return json.dumps(response)


if __name__ == '__main__':
    app.run()

# Available Hotels API

```
Takes in fromDate, toDate, city and numberOfAdults as Input and returns the list of hotels fetched from different providers
```

This code contains mainly below files:
1. **app.py** - This contains the front end APIs. Runs a flask app
2. **hotels_utils.py** - Holds the core logic to instantiate objects of different providers' classes and call their api
3. **request_wrapper.py** - Takes care of the HTTP request.
4. **proviers directory** - Holds implementation of the provider APIs.

## Running the code
Please type in the below command after navigating in terminal to directory named **available_hotels**

``` 
pip install -r requirements.txt
python app.py
```

## Calling the API
```
POST /get_hotels/ HTTP/1.1
Host: 127.0.0.1:5000
Content-Type: application/json
Cache-Control: no-cache

{
	"fromDate": "2018-09-10",
	"toDate": "2018-09-15",
	"city": "DXB",
	"numberOfAdults": 2
}
```

## Environment Variables:
>*Two Envionment variables are required in Order to run the code*
```
CRAZY_HOTELS_URL - URL to the API of provider Crazy Hotels
BEST_HOTELS_URL - URL to the API of provider Best Hotels
```

## Test Cases:
>*Test cases are still very preliminary, resided in tests directory*
```
test_besthotels.py - For Best Hotels implementation
test_crazyhotels.py - For Crazy Hotels implementation
test_hotelsUtil.py - For Out utility file hotels_util.py
```


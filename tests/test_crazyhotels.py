import json
from unittest import TestCase, main
from unittest.mock import patch
from providers.crazy_hotels import Crazyhotels


class TestCrazyhotels(TestCase):
    def setUp(self):
        self.crazy_hotels = Crazyhotels()

    def test_get_hotels(self):
        with patch("providers.crazy_hotels.RequestWrapper.make_request") as mocked:
            mocked.return_value.ok = True
            mocked.return_value.text = json.dumps([{
                "hotelName": "FiveStar",
                "price": 1500,
                "discount": 1600,
                "amenities": ["pool", "gym"],
                "rate": "*****"
            }])

            hotels = self.crazy_hotels.format_response(mocked.return_value)

            expected_output = [{
                "provider": "Crazy Hotels",
                "hotelName": "FiveStar",
                "fare": 0,
                "amenities": ["pool","gym"],
                "rate": 5
            }]

            self.assertEqual(len(hotels), len(expected_output))
            self.assertDictEqual(hotels[0], expected_output[0])

            mocked.return_value.ok = False

            hotels = self.crazy_hotels.format_response(mocked.return_value)
            self.assertEqual(len(hotels), 0)


if __name__ == "__main__":
    main()

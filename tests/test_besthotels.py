import json
from unittest import TestCase, main
from unittest.mock import patch
from providers.best_hotels import Besthotels


class TestBesthotels(TestCase):
    def setUp(self):
        self.best_hotels = Besthotels()

    def test_get_hotels(self):
        with patch("providers.best_hotels.RequestWrapper.make_request") as mocked:
            mocked.return_value.ok = True
            mocked.return_value.text = json.dumps([{
                "hotel": "FiveStar",
                "hotelFare": 1500,
                "roomAmenities": "pool,gym",
                "hotelRate": 5
            }])

            hotels = self.best_hotels.format_response(mocked.return_value)

            expected_output = [{
                "provider": "Best Hotels",
                "hotelName": "FiveStar",
                "fare": 1500,
                "amenities": ["pool","gym"],
                "rate": 5
            }]

            self.assertEqual(len(hotels), len(expected_output))
            self.assertDictEqual(hotels[0], expected_output[0])

            mocked.return_value.ok = False

            hotels = self.best_hotels.format_response(mocked.return_value)
            self.assertEqual(len(hotels), 0)


if __name__ == "__main__":
    main()

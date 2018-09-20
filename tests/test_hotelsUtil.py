import json
from unittest import TestCase, main
from hotels_util import HotelsUtil
from providers.best_hotels import Besthotels


class TestHotelsUtil(TestCase):
    def test_get_provider(self):
        hotels_util = HotelsUtil(["best_hotels"])
        self.assertEqual(type(hotels_util.get_provider("not_implemented")), type(eval('None')))
        self.assertEqual(type(hotels_util.get_provider("best_hotels")), Besthotels)


if __name__ == "__main__":
    main()

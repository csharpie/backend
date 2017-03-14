from django.test import TestCase
from api.models import Location


class TestViews(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.test_location = Location.objects.create(
            name='Spring Street Community Garden',
            latitude=34.0444447, longitude=-118.2965976,
            category='Community Garden')

    def test_fetches_index(self):
        response = self.client.get('/locations/')
        self.assertEqual(200, response.status_code)
        self.assertEqual(1, len(response.json()))
        self.assertEqual('Spring Street Community Garden',
                         response.json()[0]['name'])

    def test_fetches_by_location(self):

        # query within radius
        response = self.client.get('/nearby_locations/', {'latitude': 34.0444447,
                                                          'longitude': -118.296597})
        self.assertEqual(200, response.status_code)
        self.assertEqual(1, len(response.json()))
        self.assertEqual('Spring Street Community Garden',
                         response.json()[0]['name'])

        # query outside of radius (Santa Monica State Beach)
        response = self.client.get('/nearby_locations/', {'latitude': 34.0051628,
                                                          'longitude': -118.5145828})
        self.assertEqual(200, response.status_code)
        self.assertEqual(0, len(response.json()))

        # query with large radius override (Baldwin Hills Scenic Overlook)
        response = self.client.get('/nearby_locations/', {'radius': 15000,
                                                          'latitude': 34.0139142,
                                                          'longitude': -118.3800862})
        self.assertEqual(200, response.status_code)
        self.assertEqual(1, len(response.json()))

        # query with small radius override(Staples Center)
        response = self.client.get('/nearby_locations/', {'radius': 1,
                                                          'latitude': 34.0371399,
                                                          'longitude': -118.2682917})
        self.assertEqual(200, response.status_code)
        self.assertEqual(0, len(response.json()))

    def test_fetches_by_category(self):

        response = self.client.get('/locations/community_gardens/')
        self.assertEqual(200, response.status_code)
        self.assertEqual(1, len(response.json()))
        self.assertEqual('Spring Street Community Garden',
                         response.json()[0]['name'])

        response = self.client.get('/locations/grocery_stores/')
        self.assertEqual(200, response.status_code)
        self.assertEqual(0, len(response.json()))

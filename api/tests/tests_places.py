import json

from django.forms import model_to_dict
from django.urls import reverse
from rest_framework import status

from rest_framework.test import APIClient, APITestCase

from user.models import User

from api.serializers.place import PlaceSerializer

from places.models import Place


class PlaceViewsetTest(APITestCase):
    """
    class de test
    """

    @classmethod  # <- setUpClass doit être une méthode de classe, attention !
    def setUpTestData(cls):
        super_user = User.objects.create_superuser(username='admin', password='sysadmin', email='')
        Place.objects.create(name='test', latitude=0.0, longitude=0.0)

    def setUp(self):
        self.super_user = User.objects.get(username='admin')
        self.client = APIClient()

        self.place = Place.objects.get(name='test')

    def test_endpoint_list(self):
        url = reverse('place-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, 200)
        place_list = json.loads(response.content)

        for place in place_list:
            id = place.get('id')
            place_model = PlaceSerializer(model_to_dict(Place.objects.get(id=id))).data
            print(place)
            print(place_model)
            print("-------------")
            self.assertEqual(place, place_model)

    def test_endpoint_create(self):
        self.assertTrue(self.client.login(username='admin', password='sysadmin'))
        url = reverse('place-list')
        data = {
            'name': 'test2',
            'longitude': 0.0,
            'latitude': 0.0,
        }

        response = self.client.post(url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        test_place = Place.objects.get(name='test2')
        self.assertTrue(test_place)

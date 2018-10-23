import json

from django.forms import model_to_dict
from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from rest_framework.test import APIClient, APITestCase

from user.models import User

from api.serializers.interest import InterestSerializer

from interests.models import Interest


class InterestViewsetTest(APITestCase):
    """
    class de test
    """

    @classmethod  # <- setUpClass doit être une méthode de classe, attention !
    def setUpTestData(cls):
        super_user = User.objects.create_superuser(username='admin', password='sysadmin', email='')
        Interest.objects.create(name='test')

    def setUp(self):
        self.super_user = User.objects.get(username='admin')
        self.client = APIClient()

        self.interest = Interest.objects.get(name='test')

    def test_endpoint_list(self):
        url = reverse('interest-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, 200)
        interest_list = json.loads(response.content)

        for interest in interest_list:
            id = interest.get('id')
            interest_model = InterestSerializer(model_to_dict(Interest.objects.get(id=id))).data
            print(interest)
            print(interest_model)
            print("-------------")
            self.assertEqual(interest, interest_model)

    def test_endpoint_create(self):
        self.assertTrue(self.client.login(username='admin', password='sysadmin'))
        url = reverse('interest-list')
        data = {
            'name': 'test2',
        }

        response = self.client.post(url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        test_interest = Interest.objects.get(name='test2')
        self.assertTrue(test_interest)

    def test_endpoint_delete(self):
        self.assertTrue(self.client.login(username='admin', password='sysadmin'))

        url = reverse('interest-detail', args=[self.interest.id])
        response = self.client.delete(url, format='json')
        print(response.data)
        self.assertEqual(response.status_code, 204)

        url = reverse('interest-list')
        response = self.client.get(url, format='json')
        print(response.data)
        self.assertEqual(response.data, [])


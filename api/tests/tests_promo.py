import datetime
import json

from django.forms import model_to_dict
from django.urls import reverse
from django.utils import timezone
from rest_framework import status

from rest_framework.test import APIClient, APITestCase

from user.models import User

from api.serializers.promo import PromoSerializer

from promo.models import Promo


class PromoViewsetTest(APITestCase):
    """
    class de test
    """

    @classmethod  # <- setUpClass doit être une méthode de classe, attention !
    def setUpTestData(cls):
        super_user = User.objects.create_superuser(username='admin', password='sysadmin', email='')
        Promo.objects.create(name='test', description='meh', start=timezone.now(), end=timezone.now(),
                             owner=super_user, validation=False)

    def setUp(self):
        self.super_user = User.objects.get(username='admin')
        self.client = APIClient()

        self.promo = Promo.objects.get(name='test')

    def test_endpoint_list(self):
        url = reverse('promo-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, 200)
        promo_list = json.loads(response.content)

        for promo in promo_list:
            id = promo.get('id')
            promo_model = PromoSerializer(Promo.objects.get(id=id)).data
            print(promo)
            print(promo_model)
            print("-------------")
            self.assertEqual(promo, promo_model)

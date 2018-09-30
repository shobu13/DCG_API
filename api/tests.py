import json

from django.forms import model_to_dict
from django.test import TestCase

import datetime

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from user.models import User


class UserViewsetTest(APITestCase):

    @classmethod  # <- setUpClass doit être une méthode de classe, attention !
    def setUpTestData(cls):
        super_user = User.objects.create_superuser(username='admin', password='sysadmin', email='')

        user = User.objects.create_user('Shobu', 'shobu13@hotmail.fr', 'AzErTy#')
        user.last_name = 'Ser\'Hao'
        user.first_name = 'Shobu'
        user.street = '11 rue de la foucherais'
        user.city = 'vezin le coquet'
        user.postal_code = '35132'
        user.phone_number = '0620788001'
        user.birth_date = datetime.datetime.now().date()
        user.save()

        user2 = User.objects.create_user('Billy', 'Billy@hotmail.fr', 'AzErTy#')
        user2.last_name = 'Mitchell'
        user2.first_name = 'Billy'
        user2.street = '11 rue de la foucherais'
        user2.city = 'vezin le coquet'
        user2.postal_code = '35132'
        user2.phone_number = '0620788001'
        user2.birth_date = datetime.datetime.now().date()
        user2.amis.add(User.objects.all()[0])
        user2.save()

    def setUp(self):
        self.user, self.user2 = User.objects.all()[1:]
        self.client = APIClient()

    def test_endpoint_list(self):
        url = reverse('user-list')
        response = self.client.get(url, format='json')
        assert response.status_code == 200
        user_list = json.loads(response.content)
        # user_test = json.loads(response.content)[0]
        # print(user_test)
        # self.assertEquals(user_test.get('id'), self.user.id)
        # self.assertEquals(user_test.get('username'), self.user.username)
        # self.assertEquals(user_test.get('first_name'), self.user.first_name)
        # self.assertEquals(user_test.get('last_name'), self.user.last_name)
        # self.assertEquals(user_test.get('is_staff'), self.user.is_staff)
        # self.assertEquals(user_test.get('last_login'), self.user.last_login)
        # assert isinstance(self.user.date_joined, datetime.datetime)
        # self.assertEquals(
        #     user_test.get('date_joined'),
        #     str(self.user.date_joined.strftime('%Y-%m-%dT%H:%M:%S.%fZ'))
        # )

        for user in user_list:
            print(user)
            id = user.get('id')
            user_model = model_to_dict(User.objects.get(id=id))
            user_model['date_joined'] = user_model.get('date_joined').strftime(
                '%Y-%m-%dT%H:%M:%S.%fZ')
            self.assertEquals(user_model.get('id'), user.get('id'))
            self.assertEquals(user_model.get('username'), user.get('username'))
            self.assertEquals(user_model.get('first_name'), user.get('first_name'))
            self.assertEquals(user_model.get('last_name'), user.get('last_name'))
            self.assertEquals(user_model.get('is_staff'), user.get('is_staff'))
            self.assertEquals(user_model.get('last_login'), user.get('last_login'))
            assert isinstance(self.user.date_joined, datetime.datetime)
            self.assertEquals(user_model.get('date_joined'), user.get('date_joined'))

    def test_endpoint_create(self):
        self.assertTrue(self.client.login(username='admin', password='sysadmin'))
        url = reverse('user-list')
        response = self.client.post(url, data={
            "password": "AzErTyUiOp#",
            "is_superuser": False,
            "username": "TestUser",
            "first_name": "test",
            "last_name": "user",
            "email": "test@user.fr",
            "is_active": True,
            "street": "11 rue de ma foucherais",
            "city": "vezin le coquet",
            "postal_code": "35132",
            "phone_number": "0620788001",
            "birth_date": datetime.datetime.now().strftime('%Y-%m-%d'),
            "groups": [],
            "user_permissions": [],
            "amis": [],
        }, format='json')
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        test_user = User.objects.get(username='TestUser')
        self.assertTrue(test_user)

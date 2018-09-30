from django.core.exceptions import ValidationError
from django.test import TestCase

import datetime

from user.models import User


class UserTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        """Méthode de classe servant à créer une BDD de test, on peut y instancier nos objets"""
        user = User.objects.create_user('Shobu13', 'shobu13@hotmail.fr', 'AzErTy#')
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
        self.user, self.user2 = User.objects.all()

    def test_password(self):
        error = ''
        try:
            # test avec un mot de passe non sécurisé
            User.objects.create(username='Shobu', password='password')
        except ValidationError as exception:
            error = exception
            print('error', error)
        self.assertEquals(type(error), ValidationError)

        error = ''
        try:
            # test avec un mot de passe sécurisé
            User.objects.create(username='Shobu2', password='dsfjpbgG#')
        except ValidationError as exception:
            error = exception
            print(error)
        self.assertEquals(type(error), type(''))

    def test_user_creation(self):
        print(User.objects.all())
        self.assertTrue(
            User.objects.filter(last_name='Ser\'Hao').exists()
        )

    def test_last_name(self):
        self.assertEqual(self.user.last_name, "Ser\'Hao")

    def test_hash_password(self):
        self.assertTrue(self.user.password != 'AzErTy#')

    def test_amis(self):
        self.assertEquals(self.user, self.user2.amis.all()[0])

from django.core.exceptions import ValidationError
from django.test import TestCase
from user.models import User


class UserTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        """Méthode de classe servant à créer une BDD de test, on peut y instancier nos objets"""
        pass

    def setUp(self):
        """méthode permettant de définir des variable globales à cette série de test."""
        pass

    def test_password(self):
        error = ''
        try:
            # test avec un mot de passe non sécurisé
            User.objects.create('Shobu', 'password')
        except ValidationError as exception:
            error = exception
        self.assertEquals(type(error), ValidationError)

        try:
            # test avec un mot de passe sécurisé
            User.objects.create('Shobu2', 'dsfjpbgG#')
        except ValidationError as exception:
            error = exception
        self.assertEquals(type(error), ValidationError)

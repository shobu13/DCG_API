from django.test import TestCase

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
        Interest.objects.create('test')

    def setUp(self):
        self.super_user = User.objects.get(username='admin')
        self.client = APIClient()

    def test_base(self):
        pass

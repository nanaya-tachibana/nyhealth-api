from rest_framework.reverse import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from rest_framework.authtoken.models import Token
import models
from main.tests import create_account


class SettingTests(APITestCase):
    def setup(self):
        user = create_account('aaa', '+8613120933999', '123')
        settings = models.Setting.objects.create(user=user)

        token = Token.objects.get(user__username='aaa')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        url = reverse('setting-detail', args=[settings.pk])
        return url

    def test_retrieve_settings(self):
        """
        Ensure we can get settings.
        """
        url = self.setup()

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_partial_update_settings(self):
        """
        Ensure we can update settings.
        """
        url = self.setup()

        data = {'birthday': '1999-10-20',
                'language': 'cn'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['birthday'].isoformat(), '1999-10-20')
        self.assertEqual(response.data['language'], 'cn')


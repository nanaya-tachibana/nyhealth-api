from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from authorization.tests import BaseTests
import models


class ProfileTests(BaseTests):

    def setup(self):
        user = self.create_account('a', '+8613122510417', '123')
        url = reverse('profile-detail', args=[user.profiles.pk])
        return user, url

    def test_retrieve_profiles(self):
        """
        Ensure we can get profiles.
        """
        user, url = self.setup()
        self.login(user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_partial_update_profiles(self):
        """
        Ensure we can update profiles.
        """
        user, url = self.setup()
        data = {'birthday': '1999-10-20', 'language': 'cn'}
        self.login(user)
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['birthday'], '1999-10-20')
        self.assertEqual(response.data['language'], 'cn')


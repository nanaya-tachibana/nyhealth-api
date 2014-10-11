from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from rest_framework.authtoken.models import Token
import models


def create_account(username, phone_number, password):
    user = models.User.objects.create_user(username, phone_number,
                                           password=password)
    Token.objects.create(user=user)
    return user


class AccountTests(APITestCase):
    def test_create_account(self):
        """
        Ensure we can create a new account object.
        """
        url = reverse('user-list')
        data = {'username': 'aaa',
                'phone_number': '+8613125510418',
                'password': '123'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_signin(self):
        """
        Ensure we can sign in.
        """
        create_account('aaa', '+8613120933999', '123')
        url = reverse('signin')
        data = {'username': 'aaa', 'password': '123'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

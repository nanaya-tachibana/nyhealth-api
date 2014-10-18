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


def fake_account():
    return [
        create_account('aaa', '+8613120933999', '123'),
        create_account('1', '+8613120933991', '123')
    ]

from relations.tests import fake_relation
from vitals.tests import fake_vitals
from vitals.tests import fake_vital_record


class AccountTests(APITestCase):

    def login(self, user):
        token = Token.objects.get(user=user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

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

    def test_permissions(self):
        """
        Ensure the permissions work correctly.
        """
        user1, user2 = fake_account()
        vitals = fake_vitals()
        r = fake_vital_record(user2, vitals[1])

        self.login(user1)
        url = reverse('user-detail', args=[user2.pk]) + 'vitals/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        fake_relation(user1, user2)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_search(self):
        """
        Ensure seaching works correctly.
        """
        user1, user2 = fake_account()

        self.login(user1)
        url = reverse('user-list') + 'search/?username=' + user2.username
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)


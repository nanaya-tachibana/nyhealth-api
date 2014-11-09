'''
Created on Nov 8, 2014

@author: nanaya
'''
from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

from app_settings import auth_model_extensions
User = get_user_model()


class BaseTests(APITestCase):

    def login(self, user):
        token = Token.objects.get(user=user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

    def create_account(self, username, phone_number, password):
        user = User.objects.create_user(username, phone_number,
                                        password=password)
        Token.objects.create(user=user)
        for e in auth_model_extensions:
            e.objects.create(user=user)
        return user


class AuthTests(BaseTests):

    def test_signup(self):
        """
        Ensure we can create a new account object.
        """
        url = reverse('signup')
        data = {'username': 'aaa',
                'phone_number': '+8613125510418',
                'password': '123'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_signin(self):
        """
        Ensure we can sign in.
        """
        self.create_account('aaa', '+8613120933999', '123')
        url = reverse('login')
        data = {'phone_number': '+8613120933999', 'password': '123'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_change_password(self):
        """
        Ensure we can change the password of a user object.
        """
        user = self.create_account('aaa', '+8613120933999', '123')
        self.login(user)
        url = reverse('password_change')
        data = {'new_password1': '222', 'new_password2': '222'}
        self.client.post(url, data, format='json')
        user = User.objects.get(pk=user.pk)
        self.assertEqual(user.check_password('222'), True)

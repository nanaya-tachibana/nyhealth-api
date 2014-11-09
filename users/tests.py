from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from authorization.tests import BaseTests


class AccountTests(BaseTests):

#    def test_permissions(self):
#        """
#        Ensure the permissions work correctly.
#        """
#        user1, user2 = fake_account()
#        vitals = fake_vitals()
#        r = fake_vital_record(user2, vitals[1])
#
#        self.login(user1)
#        url = reverse('user-detail', args=[user2.pk]) + 'vitals/'
#        response = self.client.get(url)
#        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
#
#        fake_relation(user1, user2)
#        response = self.client.get(url)
#        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_search(self):
        """
        Ensure seaching works correctly.
        """
        user1, user2 = (self.create_account('aaa', '+8613120933999', '123'),
                        self.create_account('1', '+8613120933991', '123'))

        self.login(user1)
        url = reverse('user-search') + '?username=' + user2.username
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_invite(self):
        """
        Ensure we can invite others.
        """
        user = self.create_account('aaa', '+8613120933999', '123')

        self.login(user)
        url = reverse('user-invite')
        data = {'username': 'bbb',
                'phone_number': '+8613125510418',
                'password': '123'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['care_relations']['count'], 1)

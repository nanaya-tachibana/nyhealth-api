from rest_framework.reverse import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from rest_framework.authtoken.models import Token
import models


def fake_relation(user, to_user):
    return [
        models.Relation.objects.create(user=user, to_user=to_user, opposite=1),
        models.Relation.objects.create(user=to_user, to_user=user, opposite=2)
    ]

from main.tests import fake_account


class SettingTests(APITestCase):

    def login(self, user):
        token = Token.objects.get(user=user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

    def fake_relation(self, user, to_user):
        return [
            models.Relation.objects.create(user=user,
                                           to_user=to_user, opposite=0),  # rout
            models.Relation.objects.create(user=to_user,
                                           to_user=user, opposite=-1)  # rin
        ]

    def test_permissions(self):
        """
        Ensure the permissions work correctly.
        """
        user, to_user = fake_account()

        url = reverse('relation-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.login(user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        rout, rin = self.fake_relation(user, to_user)
        url = reverse('incoming-relation-detail', args=[rin.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.login(to_user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_outgoing_relation(self):
        """
        Ensure we can create a new outgoing relation.
        """
        user, to_user = fake_account()
        self.login(user)

        data = {'to_user': reverse('user-detail', args=[to_user.pk]),
                'description': 'xxxx'}

        url = reverse('outgoing-relation-list')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertQuerysetEqual(
            models.Relation.objects.filter(user=to_user,
                                           to_user=user, opposite=-1),
            ['<Relation: Relation object>'])

        url = reverse('outgoing-relation-list')
        response = self.client.get(url)

    def test_deny_incoming_relation(self):
        """
        Ensure denying a incoming relation works correctly.
        """
        user, to_user = fake_account()
        rout, rin = self.fake_relation(user, to_user)

        url = reverse('incoming-relation-detail', args=[rin.pk])
        self.login(to_user)
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertQuerysetEqual(
            models.Relation.objects.filter(user=user,
                                           to_user=to_user, opposite=-1),
            [])
        self.assertQuerysetEqual(
            models.Relation.objects.filter(user=to_user,
                                           to_user=user, opposite=0),
            [])

    def test_allow_incoming_relation(self):
        """
        Ensure allowing a incoming relation works correctly.
        """
        user, to_user = fake_account()
        rout, rin = self.fake_relation(user, to_user)

        url = reverse('incoming-relation-detail', args=[rin.pk])
        self.login(to_user)
        response = self.client.patch(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertQuerysetEqual(
            models.Relation.objects.filter(user=user,
                                           to_user=to_user, opposite=rin.pk),
            ['<Relation: Relation object>'])
        self.assertQuerysetEqual(
            models.Relation.objects.filter(user=to_user,
                                           to_user=user, opposite=rout.pk),
            ['<Relation: Relation object>'])

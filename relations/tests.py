from rest_framework.reverse import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from rest_framework.authtoken.models import Token
import models
from main.tests import create_account


class SettingTests(APITestCase):
    def setup(self):
        self.user = create_account('aaa', '+8613120933999', '123')

        token = Token.objects.get(user__username='aaa')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

    def test_create_outgoing_relation(self):
        """
        Ensure we can create a new outgoing relation.
        """
        url = reverse('outgoing-relation-list')
        self.setup()

        to_user = create_account('1', '+8613120933991', '123')
        data = {'to_user': reverse('user-detail', args=[to_user.pk]),
                'description': 'xxxx'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertQuerysetEqual(
            models.Relation.objects.filter(to_user=self.user,
                                           user=to_user, opposite=-1),
            ['<Relation: Relation object>'])

    def test_deny_incoming_relation(self):
        """
        Ensure denying a incoming relation works correctly.
        """
        self.setup()

        to_user = create_account('1', '+8613120933991', '123')
        rout = models.Relation.objects.create(to_user=self.user,
                                              user=to_user, opposite=0)
        rin = models.Relation.objects.create(user=self.user,
                                             to_user=to_user, opposite=-1)

        url = reverse('incoming-relation-detail', args=[rin.pk])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertQuerysetEqual(
            models.Relation.objects.filter(user=self.user,
                                           to_user=to_user, opposite=-1),
            [])
        self.assertQuerysetEqual(
            models.Relation.objects.filter(to_user=self.user,
                                           user=to_user, opposite=0),
            [])

    def test_allow_incoming_relation(self):
        """
        Ensure allowing a incoming relation works correctly.
        """
        self.setup()

        to_user = create_account('1', '+8613120933991', '123')
        rout = models.Relation.objects.create(to_user=self.user,
                                       user=to_user, opposite=0)
        rin = models.Relation.objects.create(user=self.user,
                                             to_user=to_user, opposite=-1)

        url = reverse('incoming-relation-detail', args=[rin.pk])
        response = self.client.patch(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertQuerysetEqual(
            models.Relation.objects.filter(user=self.user,
                                           to_user=to_user, opposite=rout.pk),
            ['<Relation: Relation object>'])
        self.assertQuerysetEqual(
            models.Relation.objects.filter(to_user=self.user,
                                           user=to_user, opposite=rin.pk),
            ['<Relation: Relation object>'])


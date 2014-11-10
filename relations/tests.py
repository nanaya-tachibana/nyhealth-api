from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APIRequestFactory

from authorization.tests import BaseTests

import models


class RelationBasedTests(BaseTests):

    def fake_relation_request(self, user, to_user):
        return [
            models.Relation.objects.create(user=user,
                                           to_user=to_user, opposite=0),  # rout
            models.Relation.objects.create(user=to_user,
                                           to_user=user, opposite=-1)  # rin
        ]

    def fake_account(self):
        return (self.create_account('aaa', '+8613120933999', '123'),
                self.create_account('1', '+8613120933991', '123'))

    def fake_relations(self, user, to_user):
        return models.Relation.build_relations(user, to_user)


class RelationTests(RelationBasedTests):

    def test_permissions(self):
        """
        Ensure the permissions work correctly.
        """
        user, to_user = self.fake_account()

        url = reverse('relation-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.login(user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        rout, rin = self.fake_relation_request(user, to_user)
        url = reverse('incoming-relation-detail', args=[rin.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.login(to_user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_outgoing_relation(self):
        """
        Ensure we can send a new outgoing request.
        """
        user, to_user = self.fake_account()
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

    def test_deny_incoming_relation(self):
        """
        Ensure denying a incoming relation works correctly.
        """
        user, to_user = self.fake_account()
        rout, rin = self.fake_relation_request(user, to_user)

        url = reverse('incoming-relation-detail', args=[rin.pk])
        self.login(to_user)
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertQuerysetEqual(
            models.Relation.objects.filter(user=user,
                                           to_user=to_user, opposite=0),
            [])
        self.assertQuerysetEqual(
            models.Relation.objects.filter(user=to_user,
                                           to_user=user, opposite=-1),
            [])

    def test_allow_incoming_relation(self):
        """
        Ensure allowing a incoming relation works correctly.
        """
        user, to_user = self.fake_account()
        rout, rin = self.fake_relation_request(user, to_user)

        url = reverse('incoming-relation-detail', args=[rin.pk])
        self.login(to_user)
        response = self.client.patch(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertQuerysetEqual(
            models.Relation.objects.filter(user=user, to_user=to_user,
                                           opposite=rin.pk),
            ['<Relation: Relation object>'])
        self.assertQuerysetEqual(
            models.Relation.objects.filter(user=to_user, to_user=user,
                                           opposite=rout.pk),
            ['<Relation: Relation object>'])

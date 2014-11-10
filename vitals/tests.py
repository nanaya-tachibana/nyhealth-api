from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from relations.tests import RelationBasedTests

import models


class VitalTests(RelationBasedTests):

    def fake_vitals(self):
        return [
            models.VitalSign.objects.create(name='a',
                                            reference_value='1', unit='1'),
            models.VitalSign.objects.create(name='b',
                                            reference_value='2', unit='1'),
            models.VitalSign.objects.create(name='c',
                                            reference_value='3', unit='2'),
            models.VitalSign.objects.create(name='aa',
                                            reference_value='1', unit='2'),
            models.VitalSign.objects.create(name='bb',
                                            reference_value='2', unit='2'),
            models.VitalSign.objects.create(name='cc',
                                            reference_value='3', unit='2')
        ]

    def fake_vital_record(self, user, vital):
        return models.UserVitalRecord.objects.create(user=user, vital=vital,
                                                     value='111')

    def test_permissions(self):
        """
        Ensure the permissions work correctly.
        """
        user1, user2 = self.fake_account()
        vitals = self.fake_vitals()

        self.fake_vital_record(user1, vitals[1])
        self.fake_vital_record(user1, vitals[2])
        record = self.fake_vital_record(user2, vitals[2])

        # user should login to view one's records
        url = reverse('vital-record-list') + '?since=1999-01-01'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # only show login user's records
        self.login(user1)
        response = self.client.get(url + '&vital=2')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

        # cannot see another user's records if they haven't build relations
        response = self.client.get(reverse('vital-record-detail',
                                           args=[record.pk]))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        response = self.client.get(url + '&user=' + str(user2.pk))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # if we are lucky to be in others carelist
        self.fake_relations(user1, user2)
        url = reverse('vital-record-one-page')
        response = self.client.get(url + '?user=' + str(user2.pk))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_upload_retrieve_records(self):
        """
        Ensure we can upload new records and get them.
        """
        user, user2 = self.fake_account()
        self.login(user)
        vitals = self.fake_vitals()
        self.fake_relations(user, user2)

        data = [
                {'user': reverse('user-detail', args=[user.pk]),
                'vital': reverse('vital-detail', args=[vitals[0].pk]),
                'value': '123'},
                {'user': reverse('user-detail', args=[user.pk]),
                'vital': reverse('vital-detail', args=[vitals[0].pk]),
                'value': '213'}
        ]
        url = reverse('vital-record-list')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # test message
        self.login(user2)
        response = self.client.get(reverse('inbox-list'))
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 2)

    def test_add_delete_monitorings(self):
        """
        Ensure we can add and delete monitorings.
        """
        user, _ = self.fake_account()
        self.login(user)
        vitals = self.fake_vitals()

        # add
        data = [
                {'user': reverse('user-detail', args=[user.pk]),
                'vital': reverse('vital-detail', args=[vitals[0].pk])},
                {'user': reverse('user-detail', args=[user.pk]),
                'vital': reverse('vital-detail', args=[vitals[1].pk])}
        ]
        url = reverse('monitoring-list')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # get
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # delete
        url = response.data['results'][0]['url']
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

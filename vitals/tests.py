from rest_framework.reverse import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from rest_framework.authtoken.models import Token
import models


def fake_vitals():
    return [
        models.VitalSign.objects.create(name='a', reference_value='1'),
        models.VitalSign.objects.create(name='b', reference_value='2'),
        models.VitalSign.objects.create(name='c', reference_value='3'),
        models.VitalSign.objects.create(name='aa', reference_value='1'),
        models.VitalSign.objects.create(name='bb', reference_value='2'),
        models.VitalSign.objects.create(name='cc', reference_value='3')

    ]


def fake_vital_record(user, vital):
    return models.UserVitalRecord.objects.create(user=user,
                                                 vital=vital, value='111')

from main.tests import fake_account


class SettingTests(APITestCase):

    def login(self, user):
        token = Token.objects.get(user=user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

    def test_permissions(self):
        """
        Ensure the permissions work correctly.
        """
        user1, user2 = fake_account()
        vitals = fake_vitals()

        fake_vital_record(user1, vitals[1])
        fake_vital_record(user1, vitals[2])
        r = fake_vital_record(user2, vitals[2])

        # user should login to view one's records
        url = reverse('vital-record-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # only show login user's records
        self.login(user1)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)

        # cannot see another user's records
        response = self.client.get(reverse('vital-record-detail', args=[r.pk]))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_upload_records(self):
        """
        Ensure we can create a new upload record.
        """
        user, _ = fake_account()
        self.login(user)
        vitals = fake_vitals()

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

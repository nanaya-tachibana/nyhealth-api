# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

from phonenumber_field.modelfields import PhoneNumberField


class UserManager(BaseUserManager):

    def _create_user(self, username, phone_number, email, password,
                     is_staff, is_superuser, **extra_fields):
        """
        Creates and saves a User with the given phone_number, 
        username and password.
        """
        if not username:
            raise ValueError('The given username must be set')
        email = self.normalize_email(email)
        user = self.model(phone_number=phone_number,
                          username=username, email=email,
                          is_staff=is_staff, is_active=True,
                          is_superuser=is_superuser,
                          **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, phone_number, email=None, password=None,
                    **extra_fields):
        return self._create_user(username, phone_number, email, password,
                                 False, False, **extra_fields)

    def create_superuser(self, username, phone_number, password, email=None,
                         **extra_fields):
        return self._create_user(username, phone_number, email, password, 
                                 True, True, **extra_fields)


class User(AbstractBaseUser):
    objects = UserManager()

    username = models.CharField(max_length=30, unique=True, db_index=True)
    phone_number = PhoneNumberField(unique=True, db_index=True)
    email = models.EmailField()
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['phone_number']

    def in_care_list(self, user_id):
        """
        Determine whether given user is in one's care list
        """
        return user_id in [r.to_user_id for r
                           in self.care_whom.filter(opposite__gt=0)]


class VitalSign(models.Model):
    name = models.CharField(max_length=60, db_index=True)
    reference_value = models.CharField(max_length=128, default='')
    created = models.DateTimeField(auto_now_add=True, db_index=True)
    updated = models.DateTimeField(
        auto_now=True, auto_now_add=True, db_index=True)


class UserSetting(models.Model):
    """
    A model representing the profiles of a user.
    """
    user = models.OneToOneField(
        User, primary_key=True, related_name='settings')
    language = models.CharField(max_length=8, default='en')
    timezone = models.CharField(max_length=8, default='UTC')

    class Meta:
        db_table = 'main_user_setting'


class UserVital(models.Model):
    """
    A model representing the vital signs of a user.
    """
    user = models.ForeignKey(User, related_name='signs', db_index=True)
    vital = models.ForeignKey(VitalSign)
    value = models.CharField(max_length=128)
    created = models.DateTimeField(auto_now_add=True, db_index=True)
    updated = models.DateTimeField(
        auto_now=True, auto_now_add=True, db_index=True)

    class Meta:
        db_table = 'main_user_vital'


class CareRelation(models.Model):
    """
    A model representing the care relations between users.

    user: An object of user who cares another user.
    to_user: An object of user who is cared by another user.
    description: A user defined description for the relation.
    opposite: The opposite relation's id.
        If it is 0, this relation is only one direction(an outgoing
        not being confirmed by another user).
    created: Created time.
    updated: Last modified time.
    """
    user = models.ForeignKey(
        User, related_name='cared_by_whom', db_index=True)
    to_user = models.ForeignKey(User, related_name='care_whom', db_index=True)
    description = models.CharField(max_length=32, default='')
    opposite = models.IntegerField(default=0, db_index=True)
    created = models.DateTimeField(auto_now_add=True, db_index=True)
    updated = models.DateTimeField(
        auto_now=True, auto_now_add=True, db_index=True)

    class Meta:
        unique_together = ('user', 'to_user')
        db_table = 'main_user_care_relation'

    @classmethod
    def get_confirmed_relations(cls, from_user):
        return cls.objects.filter(user=from_user, opposite__gt=0)

    @classmethod
    def get_outgoing_requests(cls, from_user):
        return cls.objects.filter(user=from_user, opposite=0)

    @classmethod
    def get_incoming_requests(cls, to_user):
        return cls.objects.filter(to_user=to_user, opposite=-1)

    def get_opposite(self, opposite=None):
        try:
            if opposite is None:
                opposite = self.opposite
            return CareRelation.objects.get(user_id=self.to_user,
                                            to_user_id=self.user,
                                            opposite=opposite)
        except CareRelation.DoesNotExist:
            return None

    def allow(self):
        """
        Allow an incoming care request.
        """
        outgoing = self.get_opposite(0)
        if outgoing is not None:
            outgoing.opposite = self.id
            self.opposite = outgoing.id
            outgoing.save()
            self.save()

    def deny(self):
        """
        Deny an incoming care request.
        """
        outgoing = self.get_opposite(0)
        if outgoing is not None:
            outgoing.delete()
        self.delete()

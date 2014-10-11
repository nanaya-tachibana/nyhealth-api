# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

from phonenumber_field.modelfields import PhoneNumberField


class UserManager(BaseUserManager):

    def _create_user(self, username, phone_number, email, password,
                     is_staff, is_superuser, **extra_fields):
        """
        Creates and saves a User with 
        the given phone_number, username and password.
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
    email = models.EmailField(blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['phone_number']

#    def in_care_list(self, user_id):
#        """
#        Determine whether given user is in one's care list
#        """
#        return user_id in [r.to_user_id for r
#                           in self.care_whom.filter(opposite__gt=0)]
    class Meta:
        db_table = 'users'

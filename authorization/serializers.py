'''
Created on Nov 8, 2014

@author: nanaya
'''
from django.contrib.auth import get_user_model
from django.conf import settings
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import authenticate
from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers
from rest_framework.authtoken.models import Token


User = get_user_model()


class SignupSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = tuple(User.REQUIRED_FIELDS) + (User.USERNAME_FIELD, 'password',)
        write_only_fields = ('password',)

    def save_object(self, obj, **kwargs):
        self.object = User.objects.create_user(**dict(self.init_data.items()))
        return self.object


class LoginSerializer(serializers.Serializer):

    phone_number = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        phone_number = attrs.get('phone_number')
        password = attrs.get('password')

        if phone_number and password:
            user = authenticate(phone_number=phone_number, password=password)

            if user:
                if not user.is_active:
                    msg = _('User account is disabled.')
                    raise serializers.ValidationError(msg)
                attrs['user'] = user
                return attrs
            else:
                msg = _('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg)
        else:
            msg = _('Must include "phone_number" and "password"')
            raise serializers.ValidationError(msg)


class TokenSerializer(serializers.ModelSerializer):
    """
    Serializer for Token model.
    """
    class Meta:
        model = Token
        fields = ('key',)


class UserDetailsSerializer(serializers.ModelSerializer):

    """
    User model w/o password
    """
    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'first_name', 'last_name')


class PasswordChangeSerializer(serializers.Serializer):

    new_password1 = serializers.CharField(max_length=128)
    new_password2 = serializers.CharField(max_length=128)

    set_password_form_class = SetPasswordForm

    def validate(self, attrs):
        request = self.context.get('request')
        self.set_password_form = \
            self.set_password_form_class(user=request.user, data=attrs)

        if not self.set_password_form.is_valid():
            self._errors = self.set_password_form.errors
            return None
        return attrs

    def save_object(self, *args):
        self.set_password_form.save()


class PasswordResetSerializer(serializers.Serializer):
    """
    Serializer for requesting a password reset e-mail.
    """
    pass


class PasswordResetConfirmSerializer(serializers.Serializer):
    """
    Serializer for requesting a password reset e-mail.
    """
    pass

from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core import exceptions
from django.db.transaction import atomic
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from backend.models import Profile


class UserSerializer(ModelSerializer):
    company = serializers.CharField(source='profile.company', required=False)

    def validate(self, attrs):
        # Strip out profile here so that User(**attrs) will not choke
        # We'll add it back at the end of the validate function
        profile = attrs.pop('profile', {})

        # Only validate password if it is in the set of data
        # If password does not exist during user creation then it will
        # raise a ValidationError on the parent class' validate function
        if 'password' in attrs:
            if self.instance:
                user = self.instance
            else:
                user = User(**attrs)

            password = attrs.get('password')
            errors = {}
            try:
                validate_password(password, user)
            # Validation error raised here is different than serializers.ValidationError
            except exceptions.ValidationError as e:
                errors['password'] = list(e.messages)

            if errors:
                raise serializers.ValidationError(errors)

        attrs['profile'] = profile
        return super().validate(attrs)

    @atomic
    def create(self, validated_data):
        profile = validated_data.pop('profile', {})
        user = super().create(validated_data)
        self._update_profile(Profile(user=user), profile)
        return user

    @atomic
    def update(self, instance, validated_data):
        profile = validated_data.pop('profile', {})
        self._update_profile(instance.profile, profile)
        return super().update(instance, validated_data)

    @classmethod
    def _update_profile(cls, profile, data):
        for k, v in data.items():
            if k in cls.Meta.profile_fields:
                setattr(profile, k, v)
        profile.save()

    class Meta:
        model = User
        fields = ('email', 'password', 'company',)
        profile_fields = ('company',)

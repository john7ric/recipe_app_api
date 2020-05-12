from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers


class UserCreateSerializer(serializers.ModelSerializer):
    """ serializer for user model"""

    class Meta:
        model = get_user_model()
        fields = ('email', 'name', 'password')
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}

    def create(self, validated_data):
        """ overriding create method to
        create a user with encryted password """
        user = get_user_model().objects.create_user(**validated_data)
        return user


class AuthTokenSerializer(serializers.Serializer):
    """ serializer for auth tocken creation"""

    email = serializers.EmailField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False)

    def validate(self, attrs):
        """ validate and authenticate user"""
        email = attrs['email']
        password = attrs['password']

        user = authenticate(
            request=self.context.get('request'),
            username=email,
            password=password)
        if not user:
            msg = _('unable to authenticate with provided creadentials')
            raise serializers.ValidationError(msg, code='authentication')

        attrs['user'] = user
        return attrs

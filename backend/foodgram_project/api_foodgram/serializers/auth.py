from django.contrib.auth import get_user_model
from rest_framework import serializers
from djoser.serializers import UserCreateSerializer, UserSerializer
from djoser.conf import settings

from users.models import Follow

# from recipes.validators import (
#     validate_forbidden_username,
#     validate_unique_case_insensitive_username,
#     validate_unique_case_insensitive_email,
#     validate_unique_case_insensitive_first_name,
#     validate_unique_case_insensitive_last_name
# )


User = get_user_model()


class CustomUserCreateSerializer(UserCreateSerializer):
    class Meta:
        model = User
        fields = tuple(User.REQUIRED_FIELDS) + (
            settings.LOGIN_FIELD,
            settings.USER_ID_FIELD,
            'password',
            'username'
        )


class CustomUserSerializer(UserSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = tuple(User.REQUIRED_FIELDS) + (
            settings.USER_ID_FIELD,
            settings.LOGIN_FIELD,
            'username',
            'is_subscribed'
        )
        read_only_fields = (settings.LOGIN_FIELD,)

    def get_is_subscribed(self, obj):
        subscriber = self.context['request'].user
        user = obj
        if Follow.objects.filter(user=user, subscriber=subscriber):
            return True
        return False

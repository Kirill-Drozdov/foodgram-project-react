from django.contrib.auth import get_user_model
from rest_framework import serializers

from recipes.validators import validate_unique_case_insensitive_username

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name')

    def validate_username(self, value):
        return validate_unique_case_insensitive_username(value)


class UserMeSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password')

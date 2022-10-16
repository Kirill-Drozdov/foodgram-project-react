# from django.contrib.auth import get_user_model
# from rest_framework import serializers
# from djoser.serializers import UserCreateSerializer

# from recipes.validators import (
#     validate_forbidden_username,
#     validate_unique_case_insensitive_username,
#     validate_unique_case_insensitive_email
# )

# # from users.models import User

# User = get_user_model()


# class CustomUserSerializer(UserCreateSerializer):
#     first_name = serializers.CharField(max_length=150, required=True)
#     last_name = serializers.CharField(max_length=150, required=True)
#     email = serializers.EmailField(required=True)

#     def validate(self, data):
#         username = data.get('username')
#         email = data.get('email')
#         try:
#             self.user = User.objects.get(
#                 username=username, email=email)
#         except User.DoesNotExist:
#             validate_forbidden_username(username)
#             validate_unique_case_insensitive_username(username)
#             validate_unique_case_insensitive_email(email)
#         return data

#     def create(self, validated_data):
#         if not validated_data.get('user'):
#             validated_data['user'] = User.objects.create(
#                 username=validated_data.get('username'),
#                 email=validated_data.get('email'))
#         return validated_data.get('user')

#     class Meta:
#         model = User
#         fields = ('email', 'id', 'username', 'first_name', 'last_name')

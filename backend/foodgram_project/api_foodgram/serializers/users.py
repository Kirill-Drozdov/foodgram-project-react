from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from users.models import Follow

User = get_user_model()


class FollowSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault()
    )
    subscriber = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=None
        # queryset=User.objects.all()
    )

    def validate(self, data):
        # if self.context['request'].user == data['subscriber']:
        #     raise serializers.ValidationError(
        #         'Подписываться на самого себя нельзя!'
        #     )
        return data

    class Meta:
        model = Follow
        fields = ('user', 'subscriber')
        read_only_fields = ('user', 'subscriber')
        validators = [
            UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=('user', 'subscriber')
            )
        ]

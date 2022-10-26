from django.contrib.auth import get_user_model
from rest_framework import serializers

from recipes.models import Recipe
from users.models import Follow

User = get_user_model()


class RecipesFieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = (
            'id',
            'name',
            'image',
            'cooking_time'
        )


class SubscribtionsSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()
    recipes = RecipesFieldSerializer(
        read_only=True,
        many=True
    )
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes',
            'recipes_count'
        )

    def get_is_subscribed(self, obj):
        return Follow.objects.filter(
            user=obj,
            subscriber=self.context['request'].user
        ).exists()

    def get_recipes_count(self, obj):
        return obj.recipes.count()


class FollowSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault()
    )
    email = serializers.SerializerMethodField()
    first_name = serializers.SerializerMethodField()
    last_name = serializers.SerializerMethodField()
    id = serializers.SerializerMethodField()
    is_subscribed = serializers.SerializerMethodField()
    recipes = RecipesFieldSerializer(
        read_only=True,
        many=True
    )
    recipes_count = serializers.SerializerMethodField()

    def validate(self, data):
        pk = self.context.get('view').kwargs.get('pk')
        user = User.objects.get(pk=pk)
        self.user = user
        subscriber = self.context['request'].user
        if user == subscriber:
            raise serializers.ValidationError(
                'Подписываться на самого себя нельзя!'
            )
        elif Follow.objects.filter(
            user=user,
            subscriber=subscriber
        ).exists():
            raise serializers.ValidationError(
                'Вы уже подписаны на этого пользователя!'
            )
        return data

    class Meta:
        model = Follow
        fields = (
            'user',
            'email',
            'first_name',
            'last_name',
            'id',
            'is_subscribed',
            'recipes',
            'recipes_count'
        )

    def get_email(self, obj):
        return self.user.email

    def get_first_name(self, obj):
        return self.user.first_name

    def get_last_name(self, obj):
        return self.user.last_name

    def get_id(self, obj):
        return self.user.pk

    def get_is_subscribed(self, obj):
        return True

    def get_recipes_count(self, obj):
        return self.user.recipes.count()

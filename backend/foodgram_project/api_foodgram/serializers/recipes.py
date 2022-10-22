from django.contrib.auth import get_user_model
from rest_framework import serializers

from recipes.models import Tag, Ingredient, Recipe, RecipeIngredientAmount
from users.models import Follow

User = get_user_model()


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('__all__')
        model = Tag


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('__all__')
        model = Ingredient


class AuthorFieldSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
        )
        model = User

    def get_is_subscribed(self, obj):
        subscriber = self.context['request'].user
        user = obj
        if Follow.objects.filter(user=user, subscriber=subscriber):
            return True
        return False


class IngredientFieldSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('ingredient', 'amount')
        # read_only_fields = ('name', 'measurement_unit')
        model = RecipeIngredientAmount


class RecipeCreateSerializer(serializers.ModelSerializer):
    author = AuthorFieldSerializer(read_only=True)
    ingredients = IngredientFieldSerializer(many=True, required=True)

    class Meta:
        fields = (
            'id',
            'author',
            'name',
            'tags',
            'ingredients',
            'text',
            'cooking_time',
            'image',
        )
        model = Recipe

    def create(self, validated_data):
        ingredients = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(**validated_data)

        for ingredient in ingredients:
            ingredient_pk = ingredient.get('id')
            current_ingredient = Ingredient.objects.get(
                pk=ingredient_pk
            )
            amount = ingredient.get('amount')
            RecipeIngredientAmount.objects.create(
                recipe=recipe,
                ingredient=current_ingredient,
                amount=amount
            )
        return recipe


class TagFieldSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('__all__')
        model = Tag


class RecipeSerializer(serializers.ModelSerializer):
    tags = TagFieldSerializer(
        read_only=True, many=True
    )
    author = AuthorFieldSerializer(read_only=True)

    class Meta:
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time',
        )
        model = Recipe

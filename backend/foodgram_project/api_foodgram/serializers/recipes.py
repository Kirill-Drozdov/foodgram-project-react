from django.contrib.auth import get_user_model
# from django.shortcuts import get_object_or_404
from rest_framework import serializers

from recipes.models import Tag, Ingredient, Recipe, IngredientAmount
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
    id = serializers.PrimaryKeyRelatedField(
        source='ingredient',
        queryset=Ingredient.objects.all()
    )

    class Meta:
        fields = ('id', 'amount')
        model = IngredientAmount


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
        tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(
            **validated_data
        )

        for tag in tags:
            recipe.tags.add(tag)

        for item in ingredients:
            current_ingredient = item.get('ingredient')
            amount = item.get('amount')
            ingredient_amount, _ = IngredientAmount.objects.get_or_create(
                ingredient=current_ingredient,
                amount=amount
            )
            recipe.ingredients.add(ingredient_amount)
        return recipe


class IngredientListFieldSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(
        source='ingredient',
        queryset=Ingredient.objects.all()
    )
    name = serializers.SerializerMethodField()
    measurement_unit = serializers.SerializerMethodField()

    class Meta:
        fields = ('id', 'name', 'measurement_unit', 'amount')
        model = IngredientAmount

    def get_name(self, obj):
        return obj.ingredient.name

    def get_measurement_unit(self, obj):
        return obj.ingredient.measurement_unit


class RecipeSerializer(serializers.ModelSerializer):
    tags = TagSerializer(
        read_only=True, many=True
    )
    ingredients = IngredientListFieldSerializer(
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

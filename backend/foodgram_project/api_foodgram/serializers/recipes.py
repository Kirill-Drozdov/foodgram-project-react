from rest_framework import serializers

from recipes.models import Tag, Ingredient, Recipe


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('__all__')
        model = Tag


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('__all__')
        model = Ingredient


class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'author',
            'name',
            'tags',
            'ingredients',
            'text',
            'cooking_time',
            'image',
            'is_favorited',
            'is_in_shopping_cart',
        )
        model = Recipe

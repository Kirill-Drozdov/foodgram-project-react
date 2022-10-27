import base64

from django.core.files.base import ContentFile
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from recipes.models import (Tag,
                            Ingredient,
                            Recipe,
                            IngredientAmount,
                            Favorite,
                            ShoppingCart)
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
        if not self.context['request'].user.is_authenticated:
            return False
        return Follow.objects.filter(
            user=obj,
            subscriber=self.context['request'].user
        ).exists()


class IngredientFieldSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(
        source='ingredient',
        queryset=Ingredient.objects.all()
    )

    class Meta:
        fields = ('id', 'amount')
        model = IngredientAmount


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        # Если полученный объект строка, и эта строка
        # начинается с 'data:image'...
        if isinstance(data, str) and data.startswith('data:image'):
            # ...начинаем декодировать изображение из base64.
            # Сначала нужно разделить строку на части.
            format, imgstr = data.split(';base64,')
            # И извлечь расширение файла.
            ext = format.split('/')[-1]
            # Затем декодировать сами данные и поместить результат в файл,
            # которому дать название по шаблону.
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)

        return super().to_internal_value(data)


class RecipeCreateSerializer(serializers.ModelSerializer):
    author = AuthorFieldSerializer(read_only=True)
    ingredients = IngredientFieldSerializer(many=True, required=True)
    image = Base64ImageField(required=True, allow_null=False)

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

    def update(self, instance, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')

        instance.name = validated_data.get('name', instance.name)
        instance.text = validated_data.get('text', instance.text)
        instance.cooking_time = validated_data.get(
            'cooking_time', instance.cooking_time)
        instance.image = validated_data.get('image', instance.image)

        instance.tags.clear()
        instance.ingredients.clear()

        for tag in tags:
            instance.tags.add(tag)

        for item in ingredients:
            current_ingredient = item.get('ingredient')
            amount = item.get('amount')
            ingredient_amount, _ = IngredientAmount.objects.get_or_create(
                ingredient=current_ingredient,
                amount=amount
            )
            instance.ingredients.add(ingredient_amount)
        instance.save()
        return instance


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
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    image = Base64ImageField(required=True, allow_null=False)

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

    def get_is_favorited(self, obj):
        if not self.context['request'].user.is_authenticated:
            return False
        return Favorite.objects.filter(
            user=self.context['request'].user,
            recipe=obj
        ).exists()

    def get_is_in_shopping_cart(self, obj):
        if not self.context['request'].user.is_authenticated:
            return False
        return ShoppingCart.objects.filter(
            user=self.context['request'].user,
            recipe=obj
        ).exists()


class FavoriteSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()
    cooking_time = serializers.SerializerMethodField()

    def validate(self, data):
        pk = self.context.get('view').kwargs.get('pk')
        recipe = get_object_or_404(Recipe, pk=pk)
        self.recipe_obj = recipe
        user = self.context['request'].user
        if Favorite.objects.filter(
            user=user,
            recipe=recipe
        ).exists():
            raise serializers.ValidationError(
                f'Рецепт {recipe.name} уже в избранном!'
            )
        return data

    class Meta:
        model = Favorite
        fields = (
            'id',
            'name',
            'image',
            'cooking_time'
        )

    def get_id(self, obj):
        return self.recipe_obj.pk

    def get_name(self, obj):
        return self.recipe_obj.name

    def get_image(self, obj):
        # return self.recipe_obj.image
        return None

    def get_cooking_time(self, obj):
        return self.recipe_obj.cooking_time


class ShoppingCartSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()
    cooking_time = serializers.SerializerMethodField()

    def validate(self, data):
        pk = self.context.get('view').kwargs.get('pk')
        recipe = get_object_or_404(Recipe, pk=pk)
        self.recipe_obj = recipe
        user = self.context['request'].user
        if ShoppingCart.objects.filter(
            user=user,
            recipe=recipe
        ).exists():
            raise serializers.ValidationError(
                f'Рецепт {recipe.name} уже в списке покупок!'
            )
        return data

    class Meta:
        model = ShoppingCart
        fields = (
            'id',
            'name',
            'image',
            'cooking_time'
        )

    def get_id(self, obj):
        return self.recipe_obj.pk

    def get_name(self, obj):
        return self.recipe_obj.name

    def get_image(self, obj):
        # return self.recipe_obj.image
        return None

    def get_cooking_time(self, obj):
        return self.recipe_obj.cooking_time

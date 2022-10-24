from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.response import Response

from recipes.models import Tag, Ingredient, Recipe
from api_foodgram.serializers.recipes import (
    TagSerializer,
    IngredientSerializer,
    RecipeSerializer,
    RecipeCreateSerializer
)


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()

    def get_serializer_class(self):
        if (self.action == 'create' or
                self.action == 'update'):
            return RecipeCreateSerializer
        return RecipeSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        author = self.request.user
        if serializer.is_valid():
            output_recipe = serializer.save(
                author=author)
            output_serializer = RecipeSerializer(
                output_recipe, context={'request': request}
            )
            return Response(
                output_serializer.data,
                status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        recipe = get_object_or_404(Recipe, pk=kwargs.get('pk'))
        serializer = self.get_serializer(
            recipe, data=request.data, partial=partial)
        author = self.request.user
        if serializer.is_valid():
            output_recipe = serializer.save(
                author=author)
            output_serializer = RecipeSerializer(
                output_recipe, context={'request': request}
            )
            return Response(
                output_serializer.data,
                status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

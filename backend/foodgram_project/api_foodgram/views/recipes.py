# from django.shortcuts import get_object_or_404
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
    # serializer_class = RecipeSerializer

    def get_serializer_class(self):
        if self.action == 'create':
            return RecipeCreateSerializer
        return RecipeSerializer

    def perform_create(self, serializer):
        author = self.request.user
        if serializer.is_valid():
            serializer.save(
                author=author)
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

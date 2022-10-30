from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status, generics, filters
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from recipes.models import Tag, Ingredient, Recipe, Favorite, ShoppingCart
from api_foodgram.serializers.recipes import (
    TagSerializer,
    IngredientSerializer,
    RecipeSerializer,
    RecipeCreateSerializer,
    FavoriteSerializer,
    ShoppingCartSerializer
)
from api_foodgram.permissions import (
    IsStaffOrAuthorOrReadOnlyPermission,
    IsAdminOrReadOnlyPermission
)
from api_foodgram.filters import RecipeFilter


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (IsAdminOrReadOnlyPermission,)


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    # permission_classes = (IsAdminOrReadOnlyPermission,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    permission_classes = (IsStaffOrAuthorOrReadOnlyPermission,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter

    def get_serializer_class(self):
        if self.action in ['create', 'update']:
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

    def perform_update(self, serializer):
        recipe = self.get_object()
        serializer = RecipeCreateSerializer(
            recipe, data=self.request.data)
        author = self.request.user
        if serializer.is_valid():
            output_recipe = serializer.save(
                author=author)
            output_serializer = RecipeSerializer(
                output_recipe, context={'request': self.request}
            )
            return Response(
                output_serializer.data,
                status=status.HTTP_200_OK
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class FavoriteAPIView(generics.CreateAPIView,
                      generics.DestroyAPIView):
    """Добавление/удаление в список избранного."""
    serializer_class = FavoriteSerializer

    def get_queryset(self):
        user = self.request.user
        new_queryset = Favorite.objects.filter(user=user)
        return new_queryset

    def perform_create(self, serializer):
        user = self.request.user
        recipe_id = self.kwargs.get('pk')
        recipe = get_object_or_404(Recipe, pk=recipe_id)
        if serializer.is_valid():
            serializer.save(
                user=user,
                recipe=recipe)
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        user = self.request.user
        recipe_id = self.kwargs.get('pk')
        recipe = get_object_or_404(Recipe, pk=recipe_id)
        instance = get_object_or_404(
            Favorite,
            user=user,
            recipe=recipe
        )
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class ShoppingCartAPIView(generics.CreateAPIView,
                          generics.DestroyAPIView):
    """Добавление/удаление в список покупок."""
    serializer_class = ShoppingCartSerializer

    def get_queryset(self):
        user = self.request.user
        new_queryset = ShoppingCart.objects.filter(user=user)
        return new_queryset

    def perform_create(self, serializer):
        user = self.request.user
        recipe_id = self.kwargs.get('pk')
        recipe = get_object_or_404(Recipe, pk=recipe_id)
        if serializer.is_valid():
            serializer.save(
                user=user,
                recipe=recipe)
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        user = self.request.user
        recipe_id = self.kwargs.get('pk')
        recipe = get_object_or_404(Recipe, pk=recipe_id)
        instance = get_object_or_404(
            ShoppingCart,
            user=user,
            recipe=recipe
        )
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

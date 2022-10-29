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
    # filter_backends = (DjangoFilterBackend,)
    # filterset_fields = ('tags__slug', 'author')

    def get_queryset(self):
        queryset = Recipe.objects.all()
        is_favorited = self.request.query_params.get('is_favorited')
        is_in_shopping_cart = self.request.query_params.get(
            'is_in_shopping_cart'
        )
        tags = self.request.query_params.get('tags')
        print(tags)
        if tags is not None:
            tag = get_object_or_404(
                Tag, slug=tags
            )
            queryset = Recipe.objects.filter(
                tags=tag
            )
            return queryset
        if is_favorited == '1' and self.request.user.is_authenticated:
            favorites = Favorite.objects.filter(
                user=self.request.user
            )
            queryset = []
            for obj in favorites:
                recipe = Recipe.objects.get(
                    pk=obj.recipe.pk
                )
                queryset.append(recipe)
            return queryset
        if is_in_shopping_cart == '1' and self.request.user.is_authenticated:
            shopping_cart = ShoppingCart.objects.filter(
                user=self.request.user
            )
            queryset = []
            for obj in shopping_cart:
                recipe = Recipe.objects.get(
                    pk=obj.recipe.pk
                )
                queryset.append(recipe)
            return queryset
        return queryset

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

from api_foodgram.filters import RecipeFilter
from api_foodgram.permissions import (IsAdminOrReadOnlyPermission,
                                      IsStaffOrAuthorOrReadOnlyPermission)
from api_foodgram.serializers.recipes import (FavoriteSerializer,
                                              IngredientSerializer,
                                              RecipeCreateSerializer,
                                              RecipeSerializer,
                                              TagSerializer)
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from recipes.models import (Favorite,
                            Ingredient,
                            Recipe,
                            Tag)
from rest_framework import filters, generics, status, viewsets
from rest_framework.response import Response


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None
    permission_classes = (IsAdminOrReadOnlyPermission,)


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None
    filter_backends = (filters.SearchFilter,)
    search_fields = ('^name',)


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

    def update(self, request, *args, **kwargs):
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
        return Favorite.objects.filter(
            user=self.request.user
        )

    def perform_create(self, serializer):
        user = self.request.user
        recipe = get_object_or_404(
            Recipe,
            pk=self.kwargs.get('pk')
        )
        if serializer.is_valid():
            serializer.save(
                user=user,
                recipe=recipe)
            headers = self.get_success_headers(serializer.data)
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED,
                headers=headers
            )
        return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        user = self.request.user
        recipe = get_object_or_404(
            Recipe,
            pk=self.kwargs.get('pk')
        )
        instance = get_object_or_404(
            Favorite,
            user=user,
            recipe=recipe
        )
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

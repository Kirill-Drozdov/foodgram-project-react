from datetime import datetime as dt

from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from rest_framework import viewsets, status, generics, filters
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from recipes.models import (
    Tag,
    Ingredient,
    Recipe,
    Favorite,
    ShoppingCart,
    IngredientAmount
)
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
        else:
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


class ShoppingCartAPIView(generics.CreateAPIView,
                          generics.DestroyAPIView):
    """Добавление/удаление в список покупок."""
    serializer_class = ShoppingCartSerializer

    def get_queryset(self):
        return ShoppingCart.objects.filter(
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
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        user = self.request.user
        recipe = get_object_or_404(
            Recipe,
            pk=self.kwargs.get('pk')
        )
        instance = get_object_or_404(
            ShoppingCart,
            user=user,
            recipe=recipe
        )
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', ])
def download_shopping_cart(request):
    user = request.user
    if not user.is_authenticated:
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    recipes = Recipe.objects.filter(
        shopping_cart__user=user
    )
    response = HttpResponse(content_type='text/plain')
    filename = f'{user.username}_shopping_cart.txt'
    response['Content-Disposition'] = f'attachment; filename={filename}'
    header = ['Foodgram project\n',
              '----------------\n'
              ]
    response.writelines(header)
    output_text = []
    products_dict = dict()
    for recipe in recipes:
        ingredients = IngredientAmount.objects.filter(
            recipes=recipe
        )
        for i in ingredients:
            name = i.ingredient.name
            amount = i.amount
            measurement_unit = i.ingredient.measurement_unit
            if products_dict.get(name, False):
                products_dict[name][0] += amount
            else:
                products_dict[name] = [amount, measurement_unit]
    for product in products_dict:
        name = product
        amount = products_dict[product][0]
        measurement_unit = products_dict[product][1]
        output_text += f'{name}({measurement_unit}) - {amount}\n'
    response.writelines(output_text)
    footer = ['----------------\n',
              f'Дата - {dt.now().date()}'
              ]
    response.writelines(footer)
    return response

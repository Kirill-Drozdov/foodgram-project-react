from datetime import datetime as dt

from api_foodgram.serializers.shopping_cart import ShoppingCartSerializer
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from recipes.models import IngredientAmount, Recipe
from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from shopping_cart.models import ShoppingCart


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
            headers = self.get_success_headers(serializer.data)
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED,
                headers=headers)
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

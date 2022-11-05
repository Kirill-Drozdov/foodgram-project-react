# from django.contrib.auth import get_user_model
# from django.shortcuts import get_object_or_404
# from rest_framework import serializers

# from recipes.models import Recipe
# from shopping_cart.models import ShoppingCart

# User = get_user_model()


# class ShoppingCartSerializer(serializers.ModelSerializer):
#     id = serializers.SerializerMethodField()
#     name = serializers.SerializerMethodField()
#     image = serializers.SerializerMethodField()
#     cooking_time = serializers.SerializerMethodField()

#     def validate(self, data):
#         pk = self.context.get('view').kwargs.get('pk')
#         recipe = get_object_or_404(Recipe, pk=pk)
#         self.recipe_obj = recipe
#         user = self.context['request'].user
#         if ShoppingCart.objects.filter(
#             user=user,
#             recipe=recipe
#         ).exists():
#             raise serializers.ValidationError(
#                 f'Рецепт {recipe.name} уже в списке покупок!'
#             )
#         return data

#     class Meta:
#         model = ShoppingCart
#         fields = (
#             'id',
#             'name',
#             'image',
#             'cooking_time'
#         )

#     def get_id(self, obj):
#         return self.recipe_obj.pk

#     def get_name(self, obj):
#         return self.recipe_obj.name

#     def get_image(self, obj):
#         return self.recipe_obj.image

#     def get_cooking_time(self, obj):
#         return self.recipe_obj.cooking_time

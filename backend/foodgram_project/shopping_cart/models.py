# from django.db import models

# from django.contrib.auth import get_user_model

# from recipes.models import Recipe

# User = get_user_model()


# class ShoppingCart(models.Model):
#     user = models.ForeignKey(
#         User,
#         on_delete=models.CASCADE,
#         related_name='shopping_cart',
#         verbose_name='Пользователь'
#     )
#     recipe = models.ForeignKey(
#         Recipe,
#         on_delete=models.CASCADE,
#         related_name='shopping_cart',
#         verbose_name='Рецепт'
#     )

#     class Meta:
#         constraints = [
#             models.UniqueConstraint(
#                 fields=('user', 'recipe'),
#                 name='unique_shopping_cart_model'
#             )
#         ]
#         verbose_name = 'Список покупок'
#         verbose_name_plural = 'Список покупок'

#     def __str__(self):
#         return f'{self.user} {self.recipe}'
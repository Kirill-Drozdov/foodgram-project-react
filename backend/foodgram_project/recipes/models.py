from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Tag(models.Model):
    name = models.CharField(
        'Название',
        max_length=100,
        unique=True
    )
    color = models.CharField(
        'Цветовой HEX-код',
        max_length=16,
        unique=True
    )
    slug = models.SlugField(
        'Slug',
        unique=True
    )

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self) -> str:
        return self.name


class Ingredients(models.Model):
    name = models.CharField(
        'Название ингредиента',
        max_length=100,
        unique=True
    )
    amount = models.IntegerField(
        'Количество'
    )
    measurement_unit = models.CharField(
        'Единица измерения',
        max_length=15,
    )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return self.name


# class Recipe(models.Model):
#     pass


# class ShoppingCart(models.Model):
#     pass


# class Favorite(models.Model):
#     pass

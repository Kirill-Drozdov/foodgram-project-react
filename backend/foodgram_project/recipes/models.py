from django.db import models
from django.contrib.auth import get_user_model

from recipes.validators import validate_amount, validate_cooking_time

User = get_user_model()


class Tag(models.Model):
    name = models.CharField(
        'Название',
        max_length=100,
        unique=True,
        db_index=True
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


class Ingredient(models.Model):
    name = models.CharField(
        'Название ингредиента',
        max_length=100,
        unique=True,
        db_index=True
    )
    amount = models.IntegerField(
        'Количество',
        validators=[validate_amount]
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


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор рецепта'
    )
    name = models.CharField(
        'Название рецепта',
        max_length=200
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name='Теги'
    )
    text = models.TextField(
        'Описание'
    )
    cooking_time = models.IntegerField(
        'Время приготовления(в минутах)',
        validators=[validate_cooking_time]
    )
    image = models.ImageField(
        'Картинка',
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


# class ShoppingCart(models.Model):
#     pass


# class Favorite(models.Model):
#     pass

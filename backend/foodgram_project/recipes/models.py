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
        blank=True,
        db_index=True
    )
    measurement_unit = models.CharField(
        'Единица измерения',
        blank=True,
        max_length=15,
    )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return self.name


class IngredientAmount(models.Model):
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE
    )
    amount = models.IntegerField(
        'Количество',
        validators=[validate_amount]
    )

    class Meta:
        verbose_name = 'Количество ингредиентов'
        verbose_name_plural = 'Количество ингредиентов'

    def __str__(self):
        return (f'{self.ingredient.name},'
                f'{self.ingredient.measurement_unit}: {self.amount}')


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
        # through='RecipeTag',
        verbose_name='Теги'
    )
    ingredients = models.ManyToManyField(
        IngredientAmount,
        related_name='recipes',
        # through='RecipeIngredientAmount',
        verbose_name='Ингредиенты',

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
        upload_to='recipes/images/',
        blank=True
    )
    # is_favorited = models.BooleanField(
    #     'В избранном',
    #     default=False
    # )
    # is_in_shopping_cart = models.BooleanField(
    #     'В списке покупок',
    #     default=False
    # )

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


# class RecipeIngredientAmount(models.Model):
#     ingredient = models.ForeignKey(
#         Ingredient,
#         on_delete=models.CASCADE
#     )
#     recipe = models.ForeignKey(
#         Recipe,
#         on_delete=models.CASCADE
#     )
#     amount = models.IntegerField(
#         'Количество',
#         validators=[validate_amount]
#     )

#     def __str__(self):
#         return f'{self.ingredient}, {self.recipe}'


class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Пользователь'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Рецепт'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=('user', 'recipe'),
                name='unique_favorite_model'
            )
        ]
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'

    def __str__(self):
        return f'{self.user} {self.recipe}'


class ShoppingCart(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='shopping_cart',
        verbose_name='Пользователь'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='shopping_cart',
        verbose_name='Рецепт'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=('user', 'recipe'),
                name='unique_shopping_cart_model'
            )
        ]
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Список покупок'

    def __str__(self):
        return f'{self.user} {self.recipe}'

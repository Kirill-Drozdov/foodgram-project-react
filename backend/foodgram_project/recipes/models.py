from colorfield.fields import ColorField
from django.contrib.auth import get_user_model
from django.db import models
from recipes.validators import validate_amount, validate_cooking_time

User = get_user_model()


class Tag(models.Model):
    name = models.CharField(
        'Название',
        max_length=100,
        unique=True,
        db_index=True
    )
    color = ColorField(
        'Цветовой HEX-код',
        max_length=7,
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
        verbose_name='Теги'
    )
    ingredients = models.ManyToManyField(
        IngredientAmount,
        related_name='recipes',
        verbose_name='Ингредиенты',
    )
    text = models.TextField(
        'Описание',
    )
    cooking_time = models.IntegerField(
        'Время приготовления(в минутах)',
        validators=[validate_cooking_time],
        blank=True
    )
    image = models.ImageField(
        'Картинка',
        upload_to='recipes/images/',
    )
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ('-pub_date',)

    def __str__(self):
        return self.name


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

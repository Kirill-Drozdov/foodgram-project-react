# Generated by Django 3.2.16 on 2022-10-22 12:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0003_auto_20221022_1247'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='ingredients',
            field=models.ManyToManyField(through='recipes.RecipeIngredientAmount', to='recipes.Ingredient', verbose_name='Ингредиенты'),
        ),
    ]

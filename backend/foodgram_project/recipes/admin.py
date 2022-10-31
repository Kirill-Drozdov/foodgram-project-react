from django.contrib import admin

from recipes.models import (
    Tag,
    Ingredient,
    IngredientAmount,
    Recipe,
    Favorite,
    ShoppingCart)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'color', 'slug')
    list_editable = ('color', 'slug')


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit')
    list_editable = ('measurement_unit',)
    list_filter = ('name',)


@admin.register(IngredientAmount)
class IngredientAmountAdmin(admin.ModelAdmin):
    list_display = ('ingredient', 'amount')
    list_editable = ('amount',)


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('author', 'name', )
    list_editable = ('name', )
    list_filter = ('author', 'name', 'tags')


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe')
    list_editable = ('recipe',)


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe')
    list_editable = ('recipe',)

from django.contrib import admin

from recipes.models import Tag, Ingredient, Recipe


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'color', 'slug')
    list_editable = ('color', 'slug')


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit')
    list_editable = ('measurement_unit',)


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('author', 'name', 'image', 'text', 'cooking_time')
    list_editable = ('name', 'image', 'text', 'cooking_time')


# @admin.register(RecipeIngredientAmount)
# class RecipeIngredientAmountAdmin(admin.ModelAdmin):
#     list_display = ('ingredient', 'recipe', 'amount')
#     list_editable = ('amount',)

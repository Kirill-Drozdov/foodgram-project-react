from django.contrib import admin

from recipes.models import Tag, Ingredients


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'color', 'slug')
    list_editable = ('color', 'slug')


@admin.register(Ingredients)
class IngredientsAdmin(admin.ModelAdmin):
    list_display = ('name', 'amount', 'measurement_unit')
    list_editable = ('amount', 'measurement_unit')

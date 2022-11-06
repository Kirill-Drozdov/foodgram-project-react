from django.contrib import admin

from shopping_cart.models import ShoppingCart


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe')
    list_editable = ('recipe',)
